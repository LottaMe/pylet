# test_runner.py

from unittest.mock import MagicMock
import pytest
from runner import Runner
from exercise import Exercise
import yaml

EXERCISE_DATA = {
    "exercises": {
        "exercise1": {"path": "exercise1", "test": False},
        "exercise2": {"path": "exercise2", "test": True},
    }
}


@pytest.fixture
def mock_interface():
    return MagicMock()


@pytest.fixture
def runner(tmp_path, mock_interface):
    exercise_info_path = tmp_path / "exercise_info.yaml"
    with open(exercise_info_path, "w") as f:
        yaml.dump(EXERCISE_DATA, f)

    return Runner(str(exercise_info_path), mock_interface)

def test_load_exercises_from_yaml(runner):
    exercises = runner.load_exercises_from_yaml()

    assert len(exercises) == 2
    assert all(isinstance(exercise, tuple) for exercise in exercises)
    assert exercises[0][0] == "exercise1"
    assert exercises[0][1] == {"path": "exercise1", "test": False}
    assert exercises[1][0] == "exercise2"
    assert exercises[1][1] == {"path": "exercise2", "test": True}

def test_parse_exercise(runner):
    mock_exercise_tuple = ('e1', {"path": "path/e1", "test": True})
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
