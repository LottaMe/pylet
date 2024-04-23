from unittest.mock import MagicMock, patch

import pytest
from components import ResultTests
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


def test_print_output_success_result(interface) -> None:
    interface.print_success = MagicMock()
    interface.print_error = MagicMock()

    mock_compile_result = ResultTests(success=True, output="We did it!!")

    interface.print_output(mock_compile_result)
    interface.print_success.assert_called_once_with(mock_compile_result.output)
    interface.print_error.assert_not_called()


def test_print_output_failure_result(interface) -> None:
    interface.print_success = MagicMock()
    interface.print_error = MagicMock()

    mock_compile_result = ResultTests(success=False, output="We failed!!")

    interface.print_output(mock_compile_result)
    interface.print_success.assert_not_called()
    interface.print_error.assert_called_once_with(mock_compile_result.output)


def test_print_progress_no_completed(interface, capsys) -> None:
    all = 5
    completed = 0

    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.neutral}>" in captured.out
    assert f"{interface.colors.error}----" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "0/5 0.0%" in captured.out


def test_print_progress_half_completed(interface, capsys) -> None:
    all = 5
    completed = 2

    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.success}##" in captured.out
    assert f"{interface.colors.neutral}>" in captured.out
    assert f"{interface.colors.error}--" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "2/5 40.0%" in captured.out


def test_print_progress_completed(interface, capsys) -> None:
    all = 2
    completed = 2
    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert "progress: " in captured.out
    assert f"{interface.colors.success}##" in captured.out
    assert f"{interface.colors.standard}" in captured.out
    assert "2/2 100.0%" in captured.out


def test_print_progress_last_exercise(interface, capsys) -> None:
    all = 3
    completed = 2
    interface.print_progress(all, completed)
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


def test_print_on_modify(interface):
    interface.clear = MagicMock()
    interface.print_progress = MagicMock()
    interface.print_output = MagicMock()
    interface.all_length = 3
    interface.completed_length = 1

    mock_compile_result = ResultTests(success=True, output="We did it!!")

    interface.print_on_modify(result=mock_compile_result)

    interface.clear.assert_called_once()
    interface.print_progress.assert_called_once_with(3, 1)
    interface.print_output.assert_called_once_with(mock_compile_result)