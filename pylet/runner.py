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

    def load_exercises_from_yaml(self) -> List:
        with open(self.exercise_info_path) as f:
            exercises = yaml.safe_load(f) 
        return list(exercises["exercises"].items())
    
    def parse_exercise(self, exercise_tuple) -> Exercise:
        return Exercise(
            path=f"exercises/{exercise_tuple[1]['path']}.py",     # parse Exercise
            test=exercise_tuple[1]["test"],
            interface=self.interface,
        )
    def get_exercises(self) -> List[Exercise]:
        final_list = []
        exercises = self.load_exercises_from_yaml()
        for exercise in exercises:
            final_list.append(
                self.parse_exercise(exercise)
            )
        return final_list
    
    # def 

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
                    self.completed_exercises.append(exercise.path)
                    

            else:
                self.interface.clear()
                self.interface.print_progress(self.exercises, self.completed_exercises)
                self.interface.print_error(compile_result.output)

                self.completed_exercises.append(exercise.watch_till_pass())

        self.interface.print_progress(self.exercises, self.completed_exercises)
        self.interface.print_course_complete()
