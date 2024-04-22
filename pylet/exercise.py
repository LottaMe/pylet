import multiprocessing as mp
import subprocess
import time
import traceback
from functools import partial

from components import CompileResult, Result, ResultTests
from interface import Interface
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class Exercise:
    def __init__(self, path: str, test: bool, interface: Interface) -> None:
        self.path = path
        self.code_str = ""
        self.interface = interface
        self.test = test

        self.wait = True
        self.result = None

    def read_code(self):
        with open(self.path, "r") as f:
            code_str = f.read()
        self.code_str = str(code_str)

    def run_compile(self) -> CompileResult:
        try:
            compile_obj = compile(self.code_str, self.path, "exec")
            exec_process = mp.Process(target=exec, args=(self.code_str,))
            return CompileResult(
                success=True,
                error_message=None,
                code_obj=compile_obj,
                exec_process=exec_process,
            )
        except Exception:
            error = traceback.format_exc()
            return CompileResult(success=False, error_message=error, code_obj=None)

    def run_tests(self) -> ResultTests:
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            return ResultTests(False, result.stdout)
        else:
            return ResultTests(True, result.stdout)

    def run_compile_and_tests(self) -> ResultTests | CompileResult:
        compile_result = self.run_compile()
        if compile_result.success:
            return self.run_tests()
        return compile_result

    def run_checks(self) -> Result:
        if self.test == True:
            test_result = self.run_compile_and_tests()
            self.wait = self.check_wait(test_result)
            self.result = test_result
        else:
            compile_result = self.run_compile()
            self.wait = self.check_wait(compile_result)
            self.result = compile_result

    def check_done_comment(self) -> bool:
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("# I AM NOT DONE") != -1:
                    return True
        return False

    def on_modified_recheck(self, event) -> None:
        if self.result.exec_process.is_alive():
            self.result.exec_process.terminate()
            self.result.exec_process.join()
        self.interface.clear()
        self.read_code()
        self.run_checks()
        self.interface.print_on_modify(self.result)

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
