import subprocess
from typing import List

from components import CompileResult, Colors


class Interface:
    def __init__(self) -> None:
        self.colors = Colors()

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
        self, all_exercises: List[str], completed_exercises: List[str]
    ) -> None:
        progress = [self.colors.success]
        progress.extend(["#" for _ in completed_exercises])
        if len(completed_exercises) < len(all_exercises):
            progress.append(f"{self.colors.neutral}>{self.colors.error}")
            progress.extend(
                ["-" for _ in all_exercises[len(completed_exercises) + 1 :]]
            )
        progress.append(self.colors.standard)
        print(
            "progress:",
            "".join(progress),
            f"{len(completed_exercises)}/{len(all_exercises)}",
            f"{round(((len(completed_exercises) / len(all_exercises)) * 100),1)}%",
        )

    def print_course_complete(self) -> None:
        print("You have completed the course!")

    def clear(self) -> None:
        subprocess.run(["clear"])

    def print_on_modify(
        self,
        compile_result: CompileResult,
        all_exercises: List[str],
        completed_exercises: List[str],
    ):
        self.clear()
        self.print_progress(all_exercises, completed_exercises)
        self.print_output(compile_result)
