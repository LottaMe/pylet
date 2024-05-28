from unittest.mock import MagicMock, patch
import zipfile

import pytest
from components import Result
from interface import Interface


@pytest.fixture
def interface():
    return Interface()


def test_print_success(interface, capsys) -> None:
    interface.print_success("yay")
    captured = capsys.readouterr()
    assert "\033[1;32m" in captured.out
    assert "Running the code was successful!" in captured.out
    assert "\033[0;0m" in captured.out
    assert "yay" in captured.out


def test_print_error(interface, capsys) -> None:
    interface.print_error("nay")
    captured = capsys.readouterr()
    assert "\033[1;31m" in captured.out
    assert (
        "Running the code failed! Please try again. Here's the output:" in captured.out
    )
    assert "\033[0;0m" in captured.out
    assert "nay" in captured.out


def test_print_progress_no_completed(interface, capsys) -> None:
    interface.all_length = 5
    interface.completed_length = 0

    interface.print_progress()
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.neutral}>" in captured.out
    assert f"{interface.colors.error}----" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "0/5 0.0%" in captured.out


def test_print_progress_half_completed(interface, capsys) -> None:
    interface.all_length = 5
    interface.completed_length = 2

    interface.print_progress()
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.success}##" in captured.out
    assert f"{interface.colors.neutral}>" in captured.out
    assert f"{interface.colors.error}--" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "2/5 40.0%" in captured.out


def test_print_progress_completed(interface, capsys) -> None:
    interface.all_length = 2
    interface.completed_length = 2

    interface.print_progress()
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.success}##" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "2/2 100.0%" in captured.out


def test_print_progress_last_exercise(interface, capsys) -> None:
    interface.all_length = 3
    interface.completed_length = 2

    interface.print_progress()
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.success}##" in captured.out
    assert f"{interface.colors.neutral}>" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "2/3 66.7%" in captured.out


def test_print_course_complete(interface, capsys) -> None:
    interface.print_course_complete()
    captured = capsys.readouterr()
    assert captured.out.strip() == "You have completed the course!"


@patch("subprocess.run")
def test_clear(mock_subprocess, interface):
    interface.clear()
    mock_subprocess.assert_called_once_with(["clear"])


def test_create_file_in_zip(interface):
    archive = MagicMock()

    path = "testexercise.py"

    interface.create_file_in_zip(archive, path)

    archive.open.assert_called_once_with(path, "w")
    archive.open.return_value.__enter__().write.assert_called_once_with("".encode())


def test_create_file_in_zip_with_content(interface):
    archive = MagicMock()

    path = "testexercise.py"
    content = 'print("hello world")'

    interface.create_file_in_zip(archive, path, content)

    archive.open.assert_called_once_with(path, "w")
    archive.open.return_value.__enter__().write.assert_called_once_with(
        content.encode()
    )
