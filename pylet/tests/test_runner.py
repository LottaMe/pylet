from unittest.mock import MagicMock, patch

import pytest
import yaml
from exercise import Exercise
from runner import Runner


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


@patch("runner.Observer")
@patch("runner.FileChangeHandler")
@patch("runner.Queue")
def test_watch(mock_queue, mock_file_change_handler, mock_observer, runner):
    # Setup Mocks for test
    mock_interface = MagicMock()
    runner.interface = mock_interface

    mock_exercises = [MagicMock(), MagicMock()]
    runner.get_exercises = MagicMock(return_value=mock_exercises)

    mock_queue_instance = mock_queue.return_value
    mock_queue_instance.empty.side_effect = [False, False]
    mock_queue_instance.get.side_effect = [True, True]

    mock_join = MagicMock()
    mock_file_change_handler_instance = mock_file_change_handler.return_value
    mock_file_change_handler_instance.process.join = mock_join

    def mock_process_start():
        mock_queue_instance.put(True)

    mock_file_change_handler_instance.process.start.side_effect = mock_process_start

    def mock_process_join():
        pass

    mock_file_change_handler_instance.process.join.side_effect = mock_process_join

    # Call method that is being tested
    runner.watch()

    # Assert expected methods were called
    mock_file_change_handler.assert_called()
    mock_observer.assert_called()

    mock_file_change_handler_instance.process.start.assert_called()
    mock_join.assert_called()

    mock_interface.print_progress.assert_called()
    mock_interface.print_course_complete.assert_called()


def test_summary(runner) -> None:

    mock_interface = MagicMock()
    runner.interface = mock_interface

    exercise1 = MagicMock()
    exercise1.check_done.return_value = True
    exercise2 = MagicMock()
    exercise2.check_done.return_value = False
    exercise3 = MagicMock()

    mock_exercises = [exercise1, exercise2, exercise3]
    runner.get_exercises = MagicMock(return_value=mock_exercises)

    runner.summary()

    exercise1.read_code.assert_called_once()
    exercise1.run_with_timeout.assert_called_once()
    exercise1.check_done.assert_called_once()

    exercise2.read_code.assert_called_once()
    exercise2.run_with_timeout.assert_called_once()
    exercise2.check_done.assert_called_once()

    # assert that loop breaks before exercise3
    exercise3.read_code.assert_not_called()
    exercise3.run_with_timeout.assert_not_called()
    exercise3.check_done.assert_not_called()

    mock_interface.create_summary_zip.assert_called_with(
        completed_exercises=[exercise1], current_exercise=exercise2
    )
