import multiprocessing
import time
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

    def load_exercises_from_yaml(self) -> List[Tuple[str, Dict[str, bool]]]:
        with open(self.exercise_info_path) as f:
            exercises = yaml.safe_load(f)
        return list(exercises["exercises"].items())

    def parse_exercise(self, exercise_tuple: Tuple[str, Dict[str, bool]]) -> Exercise:
        path = f"exercises/{exercise_tuple[1]['path']}.py"
        return Exercise(
            path=path,
            test=exercise_tuple[1]["test"],
            interface=self.interface,
        )

    def get_exercises(self) -> List[Exercise]:
        final_list = []
        exercises = self.load_exercises_from_yaml()
        for exercise in exercises:
            final_list.append(self.parse_exercise(exercise))
        return final_list

    def run(self) -> None:
        all_exercises = self.get_exercises()
        self.interface.all_length = len(all_exercises)
        for exercise in all_exercises:
            observer = Observer()
            queue = multiprocessing.Queue()
            filechangehandler = FileChangeHandler(exercise, PyletProcess(exercise, queue), queue)
            observer.schedule(filechangehandler, exercise.path, recursive=True)
            observer.start()

            try:
                filechangehandler.process.start()
                filechangehandler.process.join()
                wait = True
                while wait:
                    if not queue.empty():
                        wait = queue.get()
                        # wait = wait_dict

            except KeyboardInterrupt:
                observer.stop()
                observer.join()
                exit(0)
            self.interface.completed_length += 1
            observer.stop()
            observer.join()
        self.interface.print_progress(
            self.interface.all_length, self.interface.completed_length
        )
        self.interface.print_course_complete()
