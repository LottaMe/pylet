from exercise import ExerciseHandler

if __name__ == "__main__":
    exercise_handler = ExerciseHandler(exercise_info_path="exercise_info.yaml")
    for e in exercise_handler.exercises:
        path = f"exercises/{e}.py"
        if exercise_handler.check_file_exists(path):
            print(e)
            result = exercise_handler.compile_exercise(path)
            if result.success == True:
                print("success", result.output)
            else:
                print("error:", result.output)
                exit = ""
                while exit != "exit":
                    exit = input()
        else:
            pass
