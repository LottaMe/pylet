from multiprocessing import Queue
import os
from typing import Dict, List, Tuple

import yaml
from exercise import Exercise
from filehandler import FileChangeHandler
from interface import Interface
from process import PyletProcess
from watchdog.observers import Observer


class Runner:
    def __init__(self, exercise_info_path: str, interface: Interface) -> None:
        self.exercise_info_path = exercise_info_path
        self.interface = interface

        self.completed_exercises = []

    def load_exercises_from_yaml(self) -> List[Tuple[str, Dict[str, any]]]:
        """
        Reads the exercises from exercise_yaml file and returns list of
        tuple with exercise name and a dict of path and test
        """
        with open(self.exercise_info_path) as f:
            exercises = yaml.safe_load(f)
        return list(exercises["exercises"].items())

    def parse_exercise(self, exercise_tuple: Tuple[str, Dict[str, any]]) -> Exercise:
        """
        Takes an exercise tuple, with the exercise name and a dict that contains
        a partial path and test. Returns parsed exercise object with those attributes.
        """
        path = f"exercises/{exercise_tuple[1]['path']}.py"
        return Exercise(
            name=exercise_tuple[0],
            path=path,
            test=exercise_tuple[1]["test"],
            interface=self.interface,
        )

    def get_exercise_info_from_path(self, path: str) -> Dict[str, str]:
        """
        Take exercise path and return dictionary with info for exercise_info.yaml.
        """
        test = "false"
        with open(f"exercises/{path}", "r") as f:
            if "def test_" in f.read():
                test = "true"
        name = path.split("/")[-1].split(".")[0]
        return {"name": name, "path": path.split(".")[0], "test": test}

    def get_exercises(self) -> List[Exercise]:
        """
        Loads exercises from yaml and parses them as Exercise objects.
        Returns a list of Exercises, parsed from the exercise_info.yaml
        """
        final_list = []
        exercises = self.load_exercises_from_yaml()
        for exercise in exercises:
            final_list.append(self.parse_exercise(exercise))
        return final_list

    def watch(self) -> None:
        """
        Load exercises, setup interface, then go through the exercises and for each:
            - setup observer, queue and filechangehandler
            - start filechangehandler process & wait for queue to get a false
            - add to completed_exercises
            - stop observer
        Message to comlete.
        """
        all_exercises = self.get_exercises()
        self.interface.all_length = len(all_exercises)
        for exercise in all_exercises:
            observer = Observer()
            queue = Queue()
            filechangehandler = FileChangeHandler(
                exercise, PyletProcess(exercise, queue), queue
            )
            observer.schedule(filechangehandler, exercise.path, recursive=True)
            observer.start()

            try:
                filechangehandler.process.start()
                filechangehandler.process.join()
                done = False
                while not done:
                    if not queue.empty():
                        done = queue.get()

            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                exit(0)
            self.interface.completed_length += 1
            observer.stop()
            observer.join()
        self.interface.print_progress()
        self.interface.print_course_complete()

    def summary(self) -> None:
        """
        Run exercises with timeout until exercise is not done, then create a summary zip file.
        """
        all_exercises = self.get_exercises()
        self.interface.all_length = len(all_exercises)

        for exercise in all_exercises:
            try:
                exercise.read_code()
                exercise.run_with_timeout()
                self.interface.clear()

                if exercise.check_done() is False:
                    break
            except:
                break
            self.interface.completed_length += 1

        self.interface.create_summary_zip(
            completed_exercises=all_exercises[: self.interface.completed_length],
            current_exercise=all_exercises[self.interface.completed_length],
        )

    def generate(self) -> None:
        print("generating...")
        # check that exercise_info.yaml does not exist
        if os.path.isfile("exercise_info.yaml"):
            # if it exists, tell user to either adjust it or remove it before generating a new one
            print("exercise_info.yaml already exists")
            exit(0)
        # go through exercises and create a list with folders and files in exercises folder -> only
        # accept folder and .py files
        exercise_dir = [f for f in sorted(os.listdir("exercises")) if "__" not in f]
        # create an empty dict/or other ordered data structure
        # -> this is supposed to be the order of exercises + include a data structure with name, path and test
        exercise_order = []
        # ask user to pick first in order
        while len(exercise_dir) > 0:
            user_input = self.interface.get_order_index(exercise_dir)
            # add picked thing to ordered data strucutre -> if its a folder, add items in that order to data structure
            if os.path.isdir(f"exercises/{exercise_dir[int(user_input)]}"):
                for exercise in [
                    f
                    for f in sorted(
                        os.listdir(f"exercises/{exercise_dir[int(user_input)]}")
                    )
                    if ".py" in f
                ]:
                    exercise_order.append(
                        self.get_exercise_info_from_path(
                            f"{exercise_dir[int(user_input)]}/{exercise}"
                        )
                    )
            else:
                exercise_order.append(
                    self.get_exercise_info_from_path(exercise_dir[int(user_input)])
                )
            # remove item from list
            exercise_dir.pop(int(user_input))

        # take ordered data structure and exercise_info.yaml from it
        # -> this way the exercise_info.yaml is only created when rest ran successfully
        print(exercise_order)
        yaml_list = ["exercises:"]
        for exercise in exercise_order:
            yaml_list.append(
                f"""  {exercise["name"]}:
    path: {exercise["path"]}
    test: {exercise["test"]}"""
            )
        yaml_list.append("")
        with open("exercise_info.yaml", "x") as f:
            f.write("\n".join(yaml_list))
