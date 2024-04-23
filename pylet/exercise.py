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
        self.result: ResultTests | CompileResult | None = None

    def run(self):
        self.read_code()
        self.result = self.run_compile()
        self.wait = self.check_wait()
        while self.wait:
            continue
    
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

    def run_compile(self) -> CompileResult:
        try:
            compile(self.code_str, self.path, "exec")
            self.execute()
            # exec_process = mp.Process(target=self.execute)
            return CompileResult(
                success=True,
                # exec_process=exec_process,
            )
        except Exception:
            error = traceback.format_exc()
            return CompileResult(success=False, error_message=error)

    # def run_tests(self) -> ResultTests:
        # result = subprocess.run(["pytest", self.path], capture_output=True, text=True)
        # if "FAILURES" in result.stdout:
        #     return ResultTests(False, result.stdout)
        # else:
        #     return ResultTests(True, result.stdout)

    # def run_compile_and_tests(self) -> ResultTests | CompileResult:
        # compile_result = self.run_compile()
        # if compile_result.success:
        #     return self.run_tests()
        # return compile_result

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
