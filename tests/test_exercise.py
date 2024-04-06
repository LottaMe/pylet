from unittest.mock import MagicMock, call, patch
import pytest
from exercise import Exercise, CompileResult

# from interface import Interface


@pytest.fixture
def mock_interface():
    return MagicMock()


@pytest.fixture
def exercise(mock_interface):
    return Exercise("mock_path", False, mock_interface)


def test_compile_success(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "We compiled!"

        result = exercise.compile()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == True
        assert result.output == "We compiled!"


def test_compile_failure(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "We failed!"

        result = exercise.compile()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == False
        assert result.output == "We failed!"


def test_run_tests_success(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "Tests succeeded :)"

        result = exercise.run_tests()

        mock_run.assert_called_once_with(
            ["pytest", "mock_path"], capture_output=True, text=True
        )
        assert result.success == True
        assert result.output == "Tests succeeded :)"


def test_run_tests_success(exercise):
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = "oh no FAILURES 0 of 1 passed"

        result = exercise.run_tests()

        mock_run.assert_called_once_with(
            ["pytest", "mock_path"], capture_output=True, text=True
        )
        assert result.success == False
        assert result.output == "oh no FAILURES 0 of 1 passed"


def test_run_exercise_no_tests_success(exercise):
    exercise.test = False
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "We compiled!"

        result = exercise.run_exercise()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == True
        assert result.output == "We compiled!"


def test_run_exercise_no_tests_failure(exercise):
    exercise.test = False
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "We failed!"

        result = exercise.run_exercise()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == False
        assert result.output == "We failed!"


def test_run_exercise_with_tests_success(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="We compiled!."),
            MagicMock(returncode=0, stdout="Tests succeeded :)"),
        ]

        result = exercise.run_exercise()

        mock_run.assert_has_calls(
            [
                call(["python", "mock_path"], capture_output=True, text=True),
                call(["pytest", "mock_path"], capture_output=True, text=True),
            ]
        )
        assert result.success == True
        assert result.output == "Tests succeeded :)"


def test_run_exercise_with_tests_compile_fails(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="We failed!"),
            MagicMock(returncode=0, stdout="Tests succeeded :)"),
        ]

        result = exercise.run_exercise()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )

        assert result.success == False
        assert result.output == "We failed!"


def test_run_exercise_with_tests_test_fails(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="We compiled!."),
            MagicMock(returncode=0, stdout="oh no FAILURES 0 of 1 passed"),
        ]

        result = exercise.run_exercise()

        mock_run.assert_has_calls(
            [
                call(["python", "mock_path"], capture_output=True, text=True),
                call(["pytest", "mock_path"], capture_output=True, text=True),
            ]
        )
        assert result.success == False
        assert result.output == "oh no FAILURES 0 of 1 passed"


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


def test_on_modified_recheck_success(exercise, mock_interface):
    exercise.interface = mock_interface
    with patch.object(exercise, "run_exercise") as mock_run_exercise:
        mock_run_exercise.return_value = CompileResult(
            success=True, output="We compiled!."
        )

        exercise.on_modified_recheck(event=None)

        mock_interface.clear.assert_called_once()
        mock_interface.print_success.assert_called_once_with("We compiled!.")


def test_on_modified_recheck_failure(exercise, mock_interface):
    exercise.interface = mock_interface
    with patch.object(exercise, "run_exercise") as mock_run_exercise:
        mock_run_exercise.return_value = CompileResult(False, "We failed!")

        exercise.on_modified_recheck(event=None)

        mock_interface.clear.assert_called_once()
        mock_interface.print_error.assert_called_once_with("We failed!")


def test_check_wait_result_failure(exercise):
    with patch.object(exercise, "run_exercise") as mock_run_exercise:
        mock_run_exercise.return_value = CompileResult(False, "We failed!")

        assert exercise.check_wait() == True


def test_check_wait_not_done_comment(exercise):
    with patch.object(exercise, "run_exercise") as mock_run_exercise:
        mock_run_exercise.return_value = CompileResult(True, "We compiled!")
        exercise.check_done_comment = MagicMock(return_value=True)

        assert exercise.check_wait() == True
        exercise.check_done_comment.assert_called_once()


def test_check_wait_result_success_and_done(exercise):
    with patch.object(exercise, "run_exercise") as mock_run_exercise:
        mock_run_exercise.return_value = CompileResult(True, "We compiled!")
        exercise.check_done_comment = MagicMock(return_value=False)

        assert exercise.check_wait() == False
        exercise.check_done_comment.assert_called_once()
