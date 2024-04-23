import multiprocessing as mp
from types import CodeType


class Result:
    def __init__(self, success: bool) -> None:
        self.success = success


class ResultTests(Result):
    def __init__(self, success: bool, output: str) -> None:
        super().__init__(success)
        self.output = output


class CompileResult(Result):
    def __init__(
        self,
        success: bool,
        error_message: str = None,
        exec_process: mp.Process = None,
    ) -> None:
        super().__init__(success)
        self.error_message = error_message
        self.exec_process = exec_process


class Colors:
    def __init__(self) -> None:
        self.standard = "\033[0;0m"
        self.error = "\033[1;31m"
        self.success = "\033[1;32m"
        self.neutral = "\033[1;33m"
