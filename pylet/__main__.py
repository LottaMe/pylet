from exercise import ExerciseHandler
from interface import Interface

if __name__ == "__main__":
    interface = Interface()
    exercise_handler = ExerciseHandler(path="exercise_info.yaml", interface=interface)

    exercise_handler.run()
