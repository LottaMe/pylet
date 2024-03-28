from .exercise import ExerciseHandler


if __name__ == '__main__':
    exercise_handler = ExerciseHandler()
    
    for e in exercise_handler.get_exercises():
        print(e)