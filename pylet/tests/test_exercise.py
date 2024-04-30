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


def test_read_code(temp_file, exercise):
    exercise.path = temp_file
    exercise.read_code()
    assert exercise.code_str == "print('Hello, world!')"


def test_run_compile_success(exercise):
    exercise.code_str = "print('Hello, world!')"
    exercise.run_compile()
    assert exercise.result.success == True
    assert exercise.result.output == None


def test_run_compile_failure(exercise):
    exercise.code_str = "print('Hello, world!)"
    exercise.run_compile()
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


def test_run_compile_and_tests_success(exercise):
    exercise.run_compile = MagicMock()
    exercise.run_compile.side_effect = setattr(exercise, "result", Result(True))
    exercise.run_tests = MagicMock()

    exercise.run_compile_and_tests()
    exercise.run_tests.side_effect = setattr(exercise, "result", Result(True, "tests work"))

    exercise.run_compile.assert_called_once()
    exercise.run_tests.assert_called_once()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == True
    assert exercise.result.output == "tests work"


def test_run_compile_and_tests_compile_failure(exercise):
    exercise.run_compile = MagicMock()
    exercise.run_compile.side_effect = setattr(exercise, "result", Result(False, "error"))
    exercise.run_tests = MagicMock()

    exercise.run_compile_and_tests()

    exercise.run_compile.assert_called_once()
    exercise.run_tests.assert_not_called()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == False
    assert exercise.result.output == "error"


def test_run_compile_and_tests_test_failure(exercise):
    exercise.run_compile = MagicMock()
    exercise.run_compile.side_effect = setattr(exercise, "result", Result(True))
    exercise.run_tests = MagicMock()

    exercise.run_compile_and_tests()
    exercise.run_tests.side_effect = setattr(exercise, "result", Result(False, "tests failed"))

    exercise.run_compile.assert_called_once()
    exercise.run_tests.assert_called_once()
    assert isinstance(exercise.result, Result)
    assert exercise.result.success == False
    assert exercise.result.output == "tests failed"


def test_check_done_comment_present(exercise, tmp_path):
    exercise_file = tmp_path / "exercise_with_done_comment.py"
    with open(exercise_file, "w") as f:
        f.write("### Remove I AM NOT DONE COMMENT TO CONTINUE ###")
        f.write("### I AM NOT DONE ###")
        f.write("print('Hello World!')")

    exercise.path = exercise_file
    assert exercise.check_done_comment() == True


def test_check_done_comment_not_present(exercise, tmp_path):
    exercise_file = tmp_path / "exercise_with_done_comment.py"
    with open(exercise_file, "w") as f:
        f.write("### Remove I AM NOT DONE COMMENT TO CONTINUE ###")
        f.write("print('Hello World!')")

    exercise.path = exercise_file
    assert exercise.check_done_comment() == False


def test_check_wait_result_failure(exercise):
    exercise.result = Result(False, "We failed!")

    assert exercise.check_wait() == True


def test_check_wait_not_done_comment(exercise):
    exercise.result = Result(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=True)

    assert exercise.check_wait() == True
    exercise.check_done_comment.assert_called_once()


def test_check_wait_result_success_and_done(exercise):
    exercise.result = Result(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=False)

    assert exercise.check_wait() == False
    exercise.check_done_comment.assert_called_once()
