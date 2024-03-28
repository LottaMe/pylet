from ..pylet.exercise import ExerciseHandler

class TestExerciseHandler():
    path = "tests/mocks/mock_exercise_info.yaml"
    def test_get_exercises(self):
        expected_exercises = ["play_piano", "listen_to_taylor_swift", "procrastinate"]
        exercise_handler = ExerciseHandler(self.path)
        assert expected_exercises == exercise_handler.exercises