from exercise import ExerciseHandler

if __name__ == "__main__":
    exercise_handler = ExerciseHandler(exercise_info_path="exercise_info.yaml")

    for e in exercise_handler.exercises:
        if exercise_handler.check_file_exists(f"exercises/{e}.py"):
            print(e)
        else:
            pass
