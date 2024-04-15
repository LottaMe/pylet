from typing import Dict, List, Tuple

import yaml
from exercise import Exercise
from interface import Interface


class Runner:
    def __init__(self, exercise_info_path: str, interface: Interface) -> None:
        self.exercise_info_path = exercise_info_path
        self.interface = interface

        self.exercises = self.get_exercises()
        self.completed_exercises = []

    def load_exercises_from_yaml(self) -> List[Tuple[str, Dict[str, bool]]]:
        with open(self.exercise_info_path) as f:
            exercises = yaml.safe_load(f)
        return list(exercises["exercises"].items())

    def parse_exercise(self, exercise_tuple: Tuple[str, Dict[str, bool]]) -> Exercise:
        return Exercise(
            path=f"exercises/{exercise_tuple[1]['path']}.py",
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
        self.interface.all_length = len(self.exercises)
        for exercise in self.exercises:
            compile_result = exercise.run_compile_and_tests()
            if exercise.check_wait(compile_result):
                self.interface.print_on_modify(
                    compile_result=compile_result,
                )
                self.completed_exercises.append(exercise.watch_till_pass())
                self.interface.completed_length+=1
            else:
                self.completed_exercises.append(exercise.path)
                self.interface.completed_length+=1

        self.interface.print_progress(len(self.exercises), len(self.completed_exercises))
        self.interface.print_course_complete()
