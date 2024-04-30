from unittest.mock import MagicMock, patch
import pytest
from filehandler import FileChangeHandler
from watchdog.events import FileModifiedEvent


def test_on_modified_process_dead():
    exercise = MagicMock()
    process = MagicMock()
    process.is_alive.return_value = False

    file_handler = FileChangeHandler(exercise, process)

    with patch("filehandler.PyletProcess"):
        event = FileModifiedEvent("mock_path")

        file_handler.on_modified(event)

        process.terminate.assert_not_called()
        process.join.assert_not_called()

        assert isinstance(file_handler.process, MagicMock)
        assert file_handler.exercise != process
        file_handler.process.start.assert_called_once()
        file_handler.process.join.assert_called_once()


def test_on_modified_process_alive():
    exercise = MagicMock()
    process = MagicMock()
    process.is_alive.return_value = True
    file_handler = FileChangeHandler(exercise, process)

    with patch("filehandler.PyletProcess"):
        event = FileModifiedEvent("mock_path")

        file_handler.on_modified(event)

        process.terminate.assert_called_once()
        process.join.assert_called_once()

        assert isinstance(file_handler.process, MagicMock)
        assert file_handler.exercise != process
        file_handler.process.start.assert_called_once()
        file_handler.process.join.assert_called_once()
