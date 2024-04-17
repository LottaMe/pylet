import subprocess
import time
from functools import partial
import traceback

from components import CompileResult
from interface import Interface
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Exercise:
    def __init__(self, path: str, test: bool, interface: Interface) -> None:
        self.path = path
        self.code = ""
        self.interface = interface
        self.test = test

        self.wait = True

    def read_code(self):
        with open(self.path, "r") as f:
            code = f.read()
        self.code = str(code)
    
    def try_compile(self):
        try:
            compile_obj = compile(self.code, self.path, "exec")
            return CompileResult(True, compile_obj)
        except Exception:
            error = traceback.format_exc()
            return CompileResult(False, error)

    def run_tests(self) -> CompileResult:
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            return CompileResult(False, result.stdout)
        else:
            return CompileResult(True, result.stdout)

    def run_compile_and_tests(self) -> CompileResult:
        if not self.test:
            compile_result = self.try_compile()
        else:
            compile_result = self.try_compile()
            if compile_result.success:
                compile_result = self.run_tests()
        self.wait = self.check_wait(compile_result)
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
        self.read_code()
        result = self.run_compile_and_tests()
        self.interface.print_on_modify(result)

    def check_wait(self, result: CompileResult) -> bool:
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
            self.run_compile_and_tests()
            while self.wait:
                time.sleep(1)
            else:
                observer.stop()
                observer.join()
                return self.path
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            exit(0)
