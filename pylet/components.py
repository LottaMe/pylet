class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output

class Colors:
    def __init__(self) -> None:
        self.standard = "\033[0;0m"
        self.error = "\033[1;31m"
        self.success = "\033[1;32m"
        self.neutral = "\033[1;33m"
