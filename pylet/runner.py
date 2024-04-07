from typing import List

import yaml
from exercise import Exercise
from interface import Interface


class Runner:
    def __init__(self, exercise_info_path, interface: Interface) -> None:
        self.exercise_info_path = exercise_info_path
        self.interface = interface

        self.exercises = self.get_exercises()
        self.completed_exercises = []

    def get_exercises(self) -> List[Exercise]:
        final_list = []
        with open(self.exercise_info_path) as f:
            exercises = yaml.safe_load(f)                   # load from yaml function
        for exercise in exercises["exercises"].items():
            final_list.append(
                Exercise(
                    path=f"exercises/{exercise[1]['path']}.py",     # parse Exercise
                    test=exercise[1]["test"],
                    interface=self.interface,
                )
            )
        return final_list

    def run(self) -> None:
        for exercise in self.exercises:
            compile_result = exercise.run_compile_and_tests()

            if compile_result.success == True:                  # exercise method that takes result and returns true/false (maybe rewrite check_wait)
                if exercise.check_done_comment():
                    self.interface.clear()
                    self.interface.print_progress(
                        self.exercises, self.completed_exercises
                    )
                    self.interface.print_success(compile_result.output)

                    self.completed_exercises.append(exercise.watch_till_pass())
                else:
                    continue

            else:
                self.interface.clear()
                self.interface.print_progress(self.exercises, self.completed_exercises)
                self.interface.print_error(compile_result.output)

                self.completed_exercises.append(exercise.watch_till_pass())

        self.interface.print_progress(self.exercises, self.completed_exercises)
        self.interface.print_course_complete()
