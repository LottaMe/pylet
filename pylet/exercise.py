from typing import List
import yaml

class ExerciseHandler:
    def get_exercises(self) -> List[str]:
        with open("exercise_info.yaml") as f:
            exercises = yaml.safe_load(f)
        return exercises["exercises"]