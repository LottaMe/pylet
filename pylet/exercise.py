import random  # needed for quiz2 to work
import subprocess
import time
import traceback

from components import Result
from interface import Interface


class Exercise:
    def __init__(self, path: str, test: bool, interface: Interface) -> None:
        self.path = path
        self.code_str = ""
        self.interface = interface
        self.test = test

        self.result: Result = Result(success=False)

    def run(self):
        self.read_code()
        if self.test:
            self.run_compile_and_tests()
            self.interface.print_output(self.result)
        else:
            self.run_compile()
            if self.result.success:
                self.execute()
            else:
                self.interface.print_error(self.result.output)
        while self.check_wait():
            time.sleep(1)
            continue

    def read_code(self) -> None:
        with open(self.path, "r") as f:
            code_str = f.read()
        self.code_str = str(code_str)

    def execute(self) -> None:
        try:
            exec(self.code_str)
            self.interface.print_success()
        except Exception:
            error = traceback.format_exc()
            self.result = Result(success=False, output=error)
            self.interface.print_error(error)

    def run_compile(self) -> None:
        try:
            compile(self.code_str, self.path, "exec")
            self.result = Result(
                success=True,
            )
        except Exception:
            error = traceback.format_exc()
            self.result = Result(success=False, output=error)

    def run_tests(self) -> Result:
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            self.result = Result(False, result.stdout)
        else:
            self.result = Result(True, result.stdout)

    def run_compile_and_tests(self) -> Result:
        self.run_compile()
        self.execute()
        if self.result.success:
            self.run_tests()

    def check_done_comment(self) -> bool:
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("# I AM NOT DONE") != -1:
                    return True
        return False

    def check_wait(self) -> bool:
        if not self.result.success:
            return True
        if self.result.success and self.check_done_comment():
            return True
        return False
