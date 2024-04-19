# # test_runner.py

from unittest.mock import MagicMock, patch

import pytest
import yaml
from components import CompileResult, ResultTests
from exercise import Exercise
from runner import Runner

# EXERCISE_DATA = {
#     "exercises": {
#         "exercise1": {"path": "exercise1", "test": False},
#         "exercise2": {"path": "exercise2", "test": True},
#     }
# }


@pytest.fixture
def mock_interface():
    return MagicMock()

@pytest.fixture
def mock_exercise_yaml(tmp_path):
    EXERCISE_DATA = {
        "exercises": {
            "exercise1": {"path": "exercise1", "test": False},
            "exercise2": {"path": "exercise2", "test": True},
        }
    }
    exercise_info_path = tmp_path / "exercise_info.yaml"
    with open(exercise_info_path, "w") as f:
        yaml.dump(EXERCISE_DATA, f)

    return exercise_info_path

@pytest.fixture
def runner(mock_interface, mock_exercise_yaml):
    return Runner(mock_exercise_yaml, mock_interface)


def test_load_exercises_from_yaml(runner):
    exercises = runner.load_exercises_from_yaml()

    assert len(exercises) == 2
    assert all(isinstance(exercise, tuple) for exercise in exercises)
    assert exercises[0][0] == "exercise1"
    assert exercises[0][1] == {"path": "exercise1", "test": False}
    assert exercises[1][0] == "exercise2"
    assert exercises[1][1] == {"path": "exercise2", "test": True}


def test_parse_exercise(runner):
    mock_exercise_tuple = ("e1", {"path": "path/e1", "test": True})
    exercise = runner.parse_exercise(mock_exercise_tuple)
    assert exercise.path == "exercises/path/e1.py"
    assert exercise.test == True
    assert exercise.interface == runner.interface


def test_get_exercises(runner):
    exercises = runner.get_exercises()

    assert len(exercises) == 2
    assert all(isinstance(exercise, Exercise) for exercise in exercises)

    assert exercises[0].path == "exercises/exercise1.py"
    assert exercises[0].test == False
    assert exercises[1].path == "exercises/exercise2.py"
    assert exercises[1].test == True


def test_run_exercises_done(runner):
    exercise1 = MagicMock()
    exercise2 = MagicMock()
    runner.get_exercises = MagicMock()
    runner.get_exercises.return_value = [exercise1, exercise2]

    exercise1.run_compile_and_tests.return_value = ResultTests(
        success=True, output="yay"
    )
    exercise1.check_wait.return_value = False
    exercise2.run_compile_and_tests.return_value = ResultTests(
        success=True, output="yay"
    )
    exercise2.check_wait.return_value = False

    runner.run()

    assert len(runner.completed_exercises) == 2
    runner.interface.print_progress.assert_called_once_with(
        2, 2
    )
    runner.interface.print_course_complete.assert_called_once()


# def test_run(runner):
#     exercise1 = MagicMock()
#     exercise2 = MagicMock()
#     runner.exercises = [exercise1, exercise2]
#     compile_result1 = CompileResult(success=True, output="yay")
#     compile_result2 = CompileResult(success=False, output="nay")

#     exercise1.run_compile_and_tests.return_value = compile_result1
#     exercise1.check_wait.return_value = False

#     exercise2.run_compile_and_tests.return_value = compile_result2
#     exercise2.check_wait.return_value = True
#     exercise2.watch_till_pass.return_value = "path2"

#     assert len(runner.completed_exercises) == 0

#     runner.run()

#     runner.interface.print_on_modify.assert_called_once_with(
#         compile_result=compile_result2
#     )
#     runner.interface.print_progress.assert_called_once_with(
#         2, 2
#     )
#     runner.interface.print_course_complete.assert_called_once()

#     assert len(runner.completed_exercises) == 2
#     assert runner.completed_exercises.pop() == "path2"
