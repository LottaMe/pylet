from unittest.mock import MagicMock, patch

import pytest
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
    assert "Remove the # I AM NOT DONE comment to continue" in captured.out


def test_print_success_with_test(interface, capsys) -> None:
    interface.print_success("yay", True)
    captured = capsys.readouterr()
    assert "\033[1;32m" in captured.out
    assert "Tests ran successfully!" in captured.out
    assert "\033[0;0m" in captured.out
    assert "yay" in captured.out
    assert "Remove the # I AM NOT DONE comment to continue" in captured.out


def test_print_failure(interface, capsys) -> None:
    interface.print_failure("nay")
    captured = capsys.readouterr()
    assert "\033[1;31m" in captured.out
    assert (
        "Running the code failed! Please try again. Here's the output:" in captured.out
    )
    assert "\033[0;0m" in captured.out
    assert "nay" in captured.out


def test_print_failure_with_test(interface, capsys) -> None:
    interface.print_failure("nay", True)
    captured = capsys.readouterr()
    assert "\033[1;31m" in captured.out
    assert "Tests failed! Please try again. Here's the output:" in captured.out
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
    assert "Congratsss!! You have completed the courssssse!" in captured.out
    assert r"""
                      __    __    __    __
                     /  \  /  \  /  \  /  \
____________________/  __\/  __\/  __\/  __\_____________________________
___________________/  /__/  /__/  /__/  /________________________________
                   | / \   / \   / \   / \  \____
                   |/   \_/   \_/   \_/   \    o \
                                           \_____/--<""" in captured.out


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


def test_create_summary_file_in_zip(interface):
    interface.all_length = 5
    interface.completed_length = 3
    interface.create_file_in_zip = MagicMock()

    archive = MagicMock()
    archive.namelist.return_value = [
        "completed/exercise1.py",
        "completed/exercise2.py",
        "exercise3.py",
    ]
    path = "./summary"

    interface.create_summary_file_in_zip(archive, path)

    expected_content = """## PROGRESS: 3/5 (60.0%)

### current: 

- [exercise3.py](./exercise3.py)

### completed: 

- [exercise1.py](./completed/exercise1.py)
- [exercise2.py](./completed/exercise2.py)
"""
    interface.create_file_in_zip.assert_called_once_with(
        archive, f"{path}/summary.md", expected_content
    )


def test_create_summary_file_in_zip_no_completed(interface):
    interface.all_length = 5
    interface.completed_length = 0
    interface.create_file_in_zip = MagicMock()

    archive = MagicMock()
    archive.namelist.return_value = ["exercise1.py"]
    path = "./summary"

    interface.create_summary_file_in_zip(archive, path)

    expected_content = """## PROGRESS: 0/5 (0.0%)

### current: 

- [exercise1.py](./exercise1.py)

### completed: 

"""
    interface.create_file_in_zip.assert_called_once_with(
        archive, f"{path}/summary.md", expected_content
    )


def test_create_summary_zip(interface):
    exercise1 = MagicMock()
    exercise1.name = "exercise1"
    exercise1.code_str = "print('exercise1')"

    exercise2 = MagicMock()
    exercise2.name = "exercise2"
    exercise2.code_str = "print('exercise2')"

    current_exercise = MagicMock()
    current_exercise.name = "exercise3"
    current_exercise.code_str = "print('exercise3')"
    completed_exercises = [exercise1, exercise2]

    interface.create_file_in_zip = MagicMock()
    interface.create_summary_file_in_zip = MagicMock()

    with patch("zipfile.ZipFile") as mock_zipfile:
        mock_archive = MagicMock()
        mock_zipfile.return_value.__enter__.return_value = mock_archive

        interface.create_summary_zip(completed_exercises, current_exercise)

        assert interface.create_file_in_zip.call_count == 3

        interface.create_file_in_zip.assert_any_call(
            mock_archive, "./summary/exercise3.py", "print('exercise3')"
        )

        interface.create_file_in_zip.assert_any_call(
            mock_archive, "./summary/completed/exercise1.py", "print('exercise1')"
        )

        interface.create_file_in_zip.assert_any_call(
            mock_archive, "./summary/completed/exercise2.py", "print('exercise2')"
        )

        interface.create_summary_file_in_zip.assert_called_once_with(
            mock_archive, "./summary"
        )
