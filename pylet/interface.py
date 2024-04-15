import subprocess
from typing import List

from components import CompileResult, Colors


class Interface:
    def __init__(self) -> None:
        self.colors = Colors()
        self.all_length = 0
        self.completed_length = 0

    def print_success(self, output: str) -> None:
        print(self.colors.success, "Compiles Successfully!", self.colors.standard)
        print()
        print(output)

    def print_error(self, output: str) -> None:
        print(self.colors.error, "Compiling failed! Please try again. Here's the output:", self.colors.standard)
        print()
        print(output)

    def print_output(self, compile_result: CompileResult) -> None:
        if compile_result.success:
            self.print_success(compile_result.output)
        else:
            self.print_error(compile_result.output)

    def print_progress(
        self, all_length: int, completed_length: int
    ) -> None:
        progress = [self.colors.success]
        progress.extend(["#" for _ in range(completed_length)])
        if completed_length < all_length:
            progress.append(f"{self.colors.neutral}>{self.colors.error}")
            progress.extend(
                ["-" for _ in range(all_length-completed_length)]
            )
        progress.append(self.colors.standard)
        print(
            "progress:",
            "".join(progress),
            f"{completed_length}/{all_length}",
            f"{round(((completed_length / all_length) * 100),1)}%",
        )

    def print_course_complete(self) -> None:
        print("You have completed the course!")

    def clear(self) -> None:
        subprocess.run(["clear"])

    def print_on_modify(
        self,
        compile_result: CompileResult,
    ):
        self.clear()
        self.print_progress(self.all_length, self.completed_length)
        self.print_output(compile_result)
