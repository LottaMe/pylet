import math  # needed for exercises to work
import random  # needed for exercises to work
import subprocess
import time  # needed for exercises to work
import traceback

from components import Result, timeout
from interface import Interface


class Exercise:
    def __init__(self, path: str, test: bool, interface: Interface) -> None:
        self.path = path
        self.code_str = ""
        self.interface = interface
        self.test = test

        self.result: Result = Result(success=False)

    def run(self, queue):
        """
        Clear terminal & print progress.
        Read code, execute code and tests, check wait and put
        result in queue.
        """
        self.interface.clear()
        self.interface.print_progress()
        print("Running exercise", self.path)

        self.read_code()

        self.run_code_str_and_tests()

        queue.put(self.check_done())

    @timeout(3)
    def run_with_timeout(self):
        """
        Executes run_code_str_and_test method. If method isn't done executing after 3 seconds,
        it raises TimeoutError.
        """
        self.run_code_str_and_tests()

    def read_code(self) -> None:
        """
        Open file at path and save it in attribute code_str.
        """
        with open(self.path, "r") as f:
            code_str = f.read()
        self.code_str = str(code_str)

    def run_code_str(self) -> None:
        """
        Try executing code_str. Set self.result to corresonding result and output success or error message.
        """
        try:
            exec(self.code_str)

            self.result = Result(success=True, output="")
            self.interface.print_success()
        except Exception:
            error = traceback.format_exc()

            self.result = Result(success=False, output=error)
            self.interface.print_error(error)

    def run_tests(self) -> Result:
        """
        Run tests on file at self.path.
        Save result as self.result.
        """
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            self.result = Result(False, result.stdout)
            self.interface.print_error(result.stdout)
        else:
            self.result = Result(True, result.stdout)
            self.interface.print_success(result.stdout)

    def run_code_str_and_tests(self) -> Result:
        """
        Run code_str. If successful and test=true, also run tests.
        """
        self.run_code_str()
        if self.test and self.result.success:
            self.run_tests()

    def check_done_comment(self) -> bool:
        """
        Check code_str for # I AM NOT DONE comment, return True if its there and False if it isn't.
        """
        if "# I AM NOT DONE" in self.code_str:
            return True
        else:
            return False

    def check_done(self) -> bool:
        """
        Check if exercise is done, and return corresponding bool.
        """
        if not self.result.success:
            return False
        if self.result.success and self.check_done_comment():
            return False
        return True
