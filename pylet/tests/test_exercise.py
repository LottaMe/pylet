from unittest.mock import MagicMock, patch

import pytest
from components import Result
from exercise import Exercise


@pytest.fixture
def mock_interface():
    return MagicMock()


@pytest.fixture
def exercise(mock_interface):
    return Exercise("mock_path", False, mock_interface)


@pytest.fixture
def temp_file(tmp_path):
    file_content = "print('Hello, world!')"
    file_path = tmp_path / "test_file.py"
    with open(file_path, "w") as f:
        f.write(file_content)
    return file_path


def test_run_with_tests(exercise):
    mock_interface = MagicMock()
    exercise.interface = mock_interface
    exercise.test = True

    exercise.read_code = MagicMock()
    exercise.run_code_str_and_tests = MagicMock()
    exercise.run_code_str = MagicMock()

    exercise.check_done = MagicMock(return_value=True)

    exercise.run(MagicMock())

    exercise.read_code.assert_called_once()
    exercise.run_code_str_and_tests.assert_called_once()
    exercise.run_code_str.assert_not_called()


def test_run_without_tests(exercise):
    mock_interface = MagicMock()
    exercise.interface = mock_interface
    exercise.test = False

    exercise.read_code = MagicMock()
    exercise.run_code_str_and_tests = MagicMock()
    exercise.run_code_str = MagicMock()

    exercise.check_done = MagicMock(return_value=True)

    exercise.run(MagicMock())

    exercise.read_code.assert_called_once()
    exercise.run_code_str_and_tests.assert_not_called()
    exercise.run_code_str.assert_called_once()


def test_read_code(temp_file, exercise):
    exercise.path = temp_file
    exercise.read_code()
    assert exercise.code_str == "print('Hello, world!')"


def test_run_code_str_success(exercise, capsys):
    exercise.code_str = "print('Hello, world!')"
    exercise.run_code_str()
    assert exercise.result.success == True
    assert exercise.result.output == ""

    captured = capsys.readouterr()
    assert captured.out.strip() == "Hello, world!"


def test_run_code_str_failure(exercise):
    exercise.code_str = "print('Hello, world!)"
    exercise.run_code_str()
    assert exercise.result.success == False
    assert exercise.result.output != None

    assert "SyntaxError" in exercise.result.output


def test_run_tests_success(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "Tests succeeded :)"

        exercise.run_tests()

        mock_run.assert_called_once_with(
            ["pytest", "mock_path"], capture_output=True, text=True
        )
        assert exercise.result.success == True
        assert exercise.result.output == "Tests succeeded :)"


def test_run_tests_failures(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "oh no FAILURES 0 of 1 passed"

        exercise.run_tests()

        mock_run.assert_called_once_with(
            ["pytest", "mock_path"], capture_output=True, text=True
        )
        assert exercise.result.success == False
        assert exercise.result.output == "oh no FAILURES 0 of 1 passed"


def test_run_code_str_and_tests_success(exercise):
    exercise.run_code_str = MagicMock()
    exercise.run_code_str.side_effect = setattr(exercise, "result", Result(True))
    exercise.run_tests = MagicMock()

    exercise.run_code_str_and_tests()
    exercise.run_tests.side_effect = setattr(
        exercise, "result", Result(True, "tests work")
    )

    exercise.run_code_str.assert_called_once()
    exercise.run_tests.assert_called_once()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == True
    assert exercise.result.output == "tests work"


def test_run_code_str_and_tests_compile_failure(exercise):
    exercise.run_code_str = MagicMock()
    exercise.run_code_str.side_effect = setattr(
        exercise, "result", Result(False, "error")
    )
    exercise.run_tests = MagicMock()

    exercise.run_code_str_and_tests()

    exercise.run_code_str.assert_called_once()
    exercise.run_tests.assert_not_called()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == False
    assert exercise.result.output == "error"


def test_run_code_str_and_tests_test_failure(exercise):
    exercise.run_code_str = MagicMock()
    exercise.run_code_str.side_effect = setattr(exercise, "result", Result(True))
    exercise.run_tests = MagicMock()

    exercise.run_code_str_and_tests()
    exercise.run_tests.side_effect = setattr(
        exercise, "result", Result(False, "tests failed")
    )

    exercise.run_code_str.assert_called_once()
    exercise.run_tests.assert_called_once()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == False
    assert exercise.result.output == "tests failed"


def test_check_done_comment_present(exercise):
    exercise.code_str = """
### Remove I AM NOT DONE COMMENT TO CONTINUE ###
### I AM NOT DONE
print('Hello World!')
"""
    assert exercise.check_done_comment() == True


def test_check_done_comment_not_present(exercise):
    exercise.code_str = """
### Remove I AM NOT DONE COMMENT TO CONTINUE ###
print('Hello World!')
"""
    assert exercise.check_done_comment() == False


def test_check_done_result_failure(exercise):
    exercise.result = Result(False, "We failed!")

    assert exercise.check_done() == False


def test_check_done_not_done_comment(exercise):
    exercise.result = Result(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=True)

    assert exercise.check_done() == False
    exercise.check_done_comment.assert_called_once()


def test_check_done_result_success_and_done(exercise):
    exercise.result = Result(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=False)

    assert exercise.check_done() == True
    exercise.check_done_comment.assert_called_once()
