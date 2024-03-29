import os
import subprocess
from typing import List
import yaml


class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output


class ExerciseHandler:
    def __init__(self, exercise_info_path: str) -> None:
        self.exercises = self.get_exercises(exercise_info_path)

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
