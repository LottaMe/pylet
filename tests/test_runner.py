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


def test_get_exercises(runner):
    exercises = runner.get_exercises()

    assert len(exercises) == 2
    assert all(isinstance(exercise, Exercise) for exercise in exercises)
