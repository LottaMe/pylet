from runner import Runner
from interface import Interface

class TestRunner:
    interface = Interface()
    path = "tests/mocks/mock_exercise_info.yaml"

    def test_get_exercises(self):
        runner = Runner(exercise_info_path=self.path, interface=self.interface)

        expected_exercises = ["play_piano", "listen_to_taylor_swift", "procrastinate"]

        assert expected_exercises == runner.get_exercises(self.path)
        assert expected_exercises == runner.exercises

    def test_run(self):
        pass