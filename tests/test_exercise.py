from ..pylet.exercise import ExerciseHandler


class TestExerciseHandler:
    path = "tests/mocks/mock_exercise_info.yaml"
    exercise_handler = ExerciseHandler(path=path)

    def test_get_exercises(self):
        expected_exercises = ["play_piano", "listen_to_taylor_swift", "procrastinate"]

        assert expected_exercises == self.exercise_handler.get_exercises(self.path)
        assert expected_exercises == self.exercise_handler.exercises

    def test_check_file_exists(self):
        expect_true = "tests/mocks/mock_exercise.py"
        expect_false = "i_am_nobody.py"

        assert self.exercise_handler.check_file_exists(expect_true) == True
        assert self.exercise_handler.check_file_exists(expect_false) == False

    def test_compile_exercise(self):
        path = "tests/mocks/mock_exercise.py"
        f = open(path, "w")
        f.write("print 'hello world'")
        f.close()

        result_fail = self.exercise_handler.compile_exercise(path)
        assert result_fail.success == False
        assert len(result_fail.output) > 0 and isinstance(result_fail.output, str)

        f = open(path, "w")
        f.write("print('hello world')")
        f.close()

        result_success = self.exercise_handler.compile_exercise(path)
        assert result_success.success == True
        assert len(result_fail.output) > 0 and isinstance(result_success.output, str)

        open(path, "w").close()
