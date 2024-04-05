# test_runner.py

from unittest.mock import MagicMock, patch
import pytest
from runner import Runner
import yaml

# Sample exercise data for testing
EXERCISE_DATA = {
    "exercises": {
        "exercise1": {"path": "exercise1", "test": "test1"},
        "exercise2": {"path": "exercise2", "test": "test2"},
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
    assert all(isinstance(exercise, MagicMock) for exercise in exercises)
