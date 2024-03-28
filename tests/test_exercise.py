from ..pylet.exercise import ExerciseHandler


class TestExerciseHandler:
    path = "tests/mocks/mock_exercise_info.yaml"

    def test_get_exercises(self):
        expected_exercises = ["play_piano", "listen_to_taylor_swift", "procrastinate"]
        exercise_handler = ExerciseHandler(self.path)
        
        assert expected_exercises == exercise_handler.exercises

    def test_check_file_exists(self):
        expect_true = "tests/mocks/test_exercise.py"
        expect_false = "i_am_nobody.py"
        exercise_handler = ExerciseHandler(self.path)

        assert exercise_handler.check_file_exists(expect_true) == True
        assert exercise_handler.check_file_exists(expect_false) == False