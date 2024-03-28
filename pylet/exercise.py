from typing import List
import yaml

class ExerciseHandler:
    def __init__(self, exercise_info_path: str) -> None:
        self.exercises = self.get_exercises(exercise_info_path)

    def get_exercises(self, path) -> List[str]:
        with open(path) as f:
            exercises = yaml.safe_load(f)
        return exercises["exercises"]