from typing import List

import yaml
from exercise import Exercise
from interface import Interface


class Runner:
    def __init__(self, exercise_info_path, interface: Interface) -> None:
        self.exercise_info_path = exercise_info_path
        self.interface = interface

        self.exercises = self.get_exercises(exercise_info_path)
        self.completed_exercises = []

    def get_exercises(self, path) -> List[str]:
        with open(path) as f:
            exercises = yaml.safe_load(f)
        return exercises["exercises"]

    def run(self) -> None:
        for exercise in self.exercises:
            exercise = Exercise(
                path=f"exercises/{exercise}.py", interface=self.interface
            )
            compile_result = exercise.compile()
            # exercise.run_tests()

            if compile_result.success == True:
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
