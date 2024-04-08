from unittest.mock import MagicMock, patch

import pytest
from components import CompileResult
from interface import Interface


@pytest.fixture
def interface():
    return Interface()


def test_print_success(interface, capsys) -> None:
    interface.print_success("yay")
    captured = capsys.readouterr()
    assert captured.out.strip() == "success: yay"


def test_print_error(interface, capsys) -> None:
    interface.print_error("nay")
    captured = capsys.readouterr()
    assert captured.out.strip() == "error: nay"


def test_print_output_success_result(interface) -> None:
    interface.print_success = MagicMock()
    interface.print_error = MagicMock()

    mock_compile_result = CompileResult(success=True, output="We did it!!")

    interface.print_output(mock_compile_result)
    interface.print_success.assert_called_once_with(mock_compile_result.output)
    interface.print_error.assert_not_called()


def test_print_output_failure_result(interface) -> None:
    interface.print_success = MagicMock()
    interface.print_error = MagicMock()

    mock_compile_result = CompileResult(success=False, output="We failed!!")

    interface.print_output(mock_compile_result)
    interface.print_success.assert_not_called()
    interface.print_error.assert_called_once_with(mock_compile_result.output)


def test_print_progress_no_completed(interface, capsys) -> None:
    all = ["1", "2", "3", "4", "5"]
    completed = []

    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert captured.out.strip() == "progress: >---- 0/5 0.0%"


def test_print_progress_half_completed(interface, capsys) -> None:
    all = ["1", "2", "3", "4", "5"]
    completed = ["1", "2"]

    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert captured.out.strip() == "progress: ##>-- 2/5 40.0%"


def test_print_progress_completed(interface, capsys) -> None:
    all = ["1", "2"]
    completed = ["1", "2"]
    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert captured.out.strip() == "progress: ## 2/2 100.0%"


def test_print_progress_last_exercise(interface, capsys) -> None:
    all = ["1", "2", "3"]
    completed = ["1", "2"]
    interface.print_progress(all, completed)
    captured = capsys.readouterr()
    assert captured.out.strip() == "progress: ##> 2/3 66.7%"


def test_print_course_complete(interface, capsys) -> None:
    interface.print_course_complete()
    captured = capsys.readouterr()
    assert captured.out.strip() == "You have completed the course!"


@patch("subprocess.run")
def test_clear(mock_subprocess, interface):
    interface.clear()
    mock_subprocess.assert_called_once_with(["clear"])
