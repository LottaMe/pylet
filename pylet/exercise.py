import subprocess
import time
from functools import partial

from interface import Interface
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output


class Exercise:
    def __init__(self, path: str, test: bool, interface: Interface) -> None:
        self.path = path
        self.interface = interface
        self.test = test

    def compile(self) -> CompileResult:
        result = subprocess.run(["python", self.path], capture_output=True, text=True)
        if result.returncode == 0:
            return CompileResult(True, result.stdout)
        else:
            return CompileResult(False, result.stderr)

    def run_tests(self) -> CompileResult:
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            return CompileResult(False, result.stdout)
        else:
            return CompileResult(True, result.stdout)

    def run_exercise(self) -> CompileResult:
        if not self.test:
            return self.compile()
        else:
            compile_result = self.compile()
            if compile_result.success:
                return self.run_tests()
            else:
                return compile_result

    def check_done_comment(self) -> bool:
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("# I AM NOT DONE") != -1:
                    return True
        return False

    def on_modified_recheck(self, event) -> None:
        self.interface.clear()
        result = self.run_exercise()
        if result.success == True:
            self.interface.print_success(result.output)
        else:
            self.interface.print_error(result.output)

    def check_wait(self) -> bool:
        result = self.run_exercise()
        if not result.success:
            return True
        if result.success and self.check_done_comment():
            return True
        return False

    def watch_till_pass(self) -> str:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = partial(self.on_modified_recheck)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()

        try:
            while self.check_wait():
                time.sleep(1)
            else:
                observer.stop()
                observer.join()
                return self.path
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            exit(0)
