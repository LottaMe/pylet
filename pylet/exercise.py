import multiprocessing as mp
import subprocess
import time
import traceback
from functools import partial

from components import CompileResult, ResultTests
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
        self.result: ResultTests | CompileResult = CompileResult(success=False)

    def run(self):
        self.read_code()
        if self.test:
            self.run_compile_and_tests()
            self.interface.print_output(self.result)
        else:
            self.run_compile()
            if self.result.success:
                self.interface.print_success()
                self.execute()
            else:
                self.interface.print_error(self.result.error_message)
        print("self.wait is", self.check_wait())
        while self.check_wait():
            print("enter check wait while loop")
            time.sleep(1)
            continue
        print("exiting while loop")
    
    def read_code(self) -> None:
        with open(self.path, "r") as f:
            code_str = f.read()
        self.code_str = str(code_str)

    def execute(self) -> None:
        try:
            exec(self.code_str)
        except Exception:
            error = traceback.format_exc()
            self.result = CompileResult(success=False, error_message=error)
            self.interface.print_error(error)

    def run_compile(self) -> None:
        try:
            compile(self.code_str, self.path, "exec")
            self.result = CompileResult(
                success=True,
            )
        except Exception:
            error = traceback.format_exc()
            self.result = CompileResult(success=False, error_message=error)

    def run_tests(self) -> ResultTests:
        result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        if "FAILURES" in result.stdout:
            self.result = ResultTests(False, result.stdout)
        else:
            self.result = ResultTests(True, result.stdout)

    def run_compile_and_tests(self) -> ResultTests | CompileResult:
        self.run_compile()
        if self.result.success:
            self.run_tests()

    # def run_checks(self) -> ResultTests | CompileResult:
        # if self.test == True:
        #     test_result = self.run_compile_and_tests()
        #     self.wait = self.check_wait(test_result)
        #     self.result = test_result
        # else:
        #     compile_result = self.run_compile()
        #     self.wait = self.check_wait(compile_result)
        #     self.result = compile_result

    def check_done_comment(self) -> bool:
        with open(self.path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("# I AM NOT DONE") != -1:
                    return True
        return False

    # def on_modified_recheck(self, event) -> None:
        # if isinstance(self.result, CompileResult) and self.result.success and self.result.exec_process.is_alive():
        #     self.result.exec_process.terminate()
        #     self.result.exec_process.join()
        # self.interface.clear()
        # self.read_code()
        # self.run_checks()
        # self.interface.print_on_modify(self.result)

    def check_wait(self) -> bool:
        if not self.result.success:
            return True
        if self.result.success and self.check_done_comment():
            return True
        return False

    # def watch_till_pass(self) -> str:
    #     event_handler = FileSystemEventHandler()
    #     event_handler.on_modified = partial(self.on_modified_recheck)
    #     observer = Observer()
    #     observer.schedule(event_handler, self.path, recursive=True)
    #     observer.start()

    #     try:
    #         while self.wait:
    #             time.sleep(1)
    #         else:
    #             observer.stop()
    #             observer.join()
    #             return self.path
    #     except KeyboardInterrupt:
    #         observer.stop()
    #         observer.join()
    #         exit(0)
