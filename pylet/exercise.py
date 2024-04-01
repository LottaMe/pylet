import os
import subprocess
from typing import List
import yaml


class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output


class ExerciseHandler:
    def __init__(self, path: str) -> None:
        self.path = path
        self.exercises = self.get_exercises(path)

    def get_exercises(self, path) -> List[str]:
        with open(path) as f:
            exercises = yaml.safe_load(f)
        return exercises["exercises"]

    def check_file_exists(self, path) -> bool:
        return os.path.isfile(path)

    def compile_exercise(self, path) -> CompileResult:
        result = subprocess.run(["python", path], capture_output=True, text=True)
        if result.returncode == 0:
            return CompileResult(True, result.stdout)
        else:
            return CompileResult(False, result.stderr)
        
    def run(self) -> None: 
        # for loop through self.exercises
        for exercise in self.exercises:
            exercise_path = f"exercises/{exercise}.py"
            # check if file exists
            if not self.check_file_exists(exercise_path):
                continue
            # check if file compiles
            compile_result = self.compile_exercise(exercise_path)
            # yes -> feedback message
            if compile_result.success == True:
                print("success:", compile_result.output)
            # no -> while loop, wait for file change/exit
            else:
                print("error:", compile_result.output)
                exit = ""
                valid_exits = ["exit", "exit()", "q"]
                while exit not in valid_exits:
                    exit = input()