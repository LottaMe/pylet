from unittest.mock import MagicMock, call, patch
import pytest
from exercise import Exercise
from components import CompileResult
from watchdog.events import FileModifiedEvent

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


def test_run_compile_and_tests_no_tests_success(exercise):
    exercise.test = False
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = "We compiled!"

        result = exercise.run_compile_and_tests()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == True
        assert result.output == "We compiled!"


def test_run_compile_and_tests_no_tests_failure(exercise):
    exercise.test = False
    with patch("subprocess.run") as mock_run:
        mock_run.return_value.returncode = 1
        mock_run.return_value.stderr = "We failed!"

        result = exercise.run_compile_and_tests()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )
        assert result.success == False
        assert result.output == "We failed!"


def test_run_compile_and_tests_with_tests_success(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="We compiled!."),
            MagicMock(returncode=0, stdout="Tests succeeded :)"),
        ]

        result = exercise.run_compile_and_tests()

        mock_run.assert_has_calls(
            [
                call(["python", "mock_path"], capture_output=True, text=True),
                call(["pytest", "mock_path"], capture_output=True, text=True),
            ]
        )
        assert result.success == True
        assert result.output == "Tests succeeded :)"


def test_run_compile_and_tests_with_tests_compile_fails(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=1, stderr="We failed!"),
            MagicMock(returncode=0, stdout="Tests succeeded :)"),
        ]

        result = exercise.run_compile_and_tests()

        mock_run.assert_called_once_with(
            ["python", "mock_path"], capture_output=True, text=True
        )

        assert result.success == False
        assert result.output == "We failed!"


def test_run_compile_and_tests_with_tests_test_fails(exercise):
    exercise.test = True
    with patch("subprocess.run") as mock_run:
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout="We compiled!."),
            MagicMock(returncode=0, stdout="oh no FAILURES 0 of 1 passed"),
        ]

        result = exercise.run_compile_and_tests()

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
    with patch.object(exercise, "run_compile_and_tests") as mock_run_compile_and_tests:
        mock_compile_result = CompileResult(success=True, output="We compiled!.")
        mock_run_compile_and_tests.return_value = mock_compile_result

        exercise.on_modified_recheck(event=None)

        mock_interface.clear.assert_called_once()
        mock_interface.print_output.assert_called_once_with(mock_compile_result)


def test_on_modified_recheck_failure(exercise, mock_interface):
    exercise.interface = mock_interface
    with patch.object(exercise, "run_compile_and_tests") as mock_run_compile_and_tests:
        mock_compile_result = CompileResult(False, "We failed!")
        mock_run_compile_and_tests.return_value = mock_compile_result

        exercise.on_modified_recheck(event=None)

        mock_interface.clear.assert_called_once()
        mock_interface.print_output.assert_called_once_with(mock_compile_result)


def test_check_wait_result_failure(exercise):
    mock_compile_result = CompileResult(False, "We failed!")

    assert exercise.check_wait(mock_compile_result) == True


def test_check_wait_not_done_comment(exercise):
    mock_compile_result = CompileResult(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=True)

    assert exercise.check_wait(mock_compile_result) == True
    exercise.check_done_comment.assert_called_once()


def test_check_wait_result_success_and_done(exercise):
    mock_compile_results = CompileResult(True, "We compiled!")
    exercise.check_done_comment = MagicMock(return_value=False)

    assert exercise.check_wait(mock_compile_results) == False
    exercise.check_done_comment.assert_called_once()


def test_watch_till_pass_succeeds(exercise):
    exercise.path = "fake_path3"
    with patch("exercise.time.sleep"), patch("exercise.Observer"), patch(
        "exercise.FileSystemEventHandler"
    ):
        with patch.object(exercise, "check_wait") as mock_check_wait:
            mock_check_wait.side_effect = [False]

            result = exercise.watch_till_pass()

            assert result == "fake_path3"


def test_watch_till_pass_modify(exercise):
    exercise.on_modified_recheck = MagicMock()
    with patch("exercise.time.sleep"), patch("exercise.Observer"), patch(
        "exercise.FileSystemEventHandler"
    ) as mock_file_system_event_handler:
        mock_event_handler_instance = mock_file_system_event_handler.return_value

        with patch.object(exercise, "check_wait") as mock_check_wait:
            mock_check_wait.side_effect = [True, False]

            exercise.watch_till_pass()

            event = FileModifiedEvent("mock_path")
            mock_event_handler_instance.on_modified(event)

            exercise.on_modified_recheck.assert_called_once()


def test_watch_till_pass_keyboard_interrupt(exercise):
    with patch("exercise.time.sleep"), patch("exercise.Observer"), patch(
        "exercise.FileSystemEventHandler"
    ):
        with patch.object(exercise, "check_wait") as mock_check_wait:
            mock_check_wait.side_effect = KeyboardInterrupt()

            try:
                exercise.watch_till_pass()
            except SystemExit:
                assert True == True
