from typing import Dict, List, Tuple

import yaml
from exercise import Exercise
from interface import Interface


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
            exercise.read_code()
            result = exercise.run_checks()
            if exercise.wait:
                self.interface.print_on_modify(result)
                self.completed_exercises.append(exercise.watch_till_pass())
                self.interface.completed_length += 1
            else:
                self.completed_exercises.append(exercise.path)
                self.interface.completed_length += 1

        self.interface.print_progress(
            len(all_exercises), len(self.completed_exercises)
        )
        self.interface.print_course_complete()
