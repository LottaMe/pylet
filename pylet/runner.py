from multiprocessing import Queue
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
            path=path,
            test=exercise_tuple[1]["test"],
            interface=self.interface,
        )

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

        self.interface.create_summary_folder(
            completed_exercises=all_exercises[:self.interface.completed_length],
            current_exercise=all_exercises[self.interface.completed_length]    
        )