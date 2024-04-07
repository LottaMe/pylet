import subprocess
from typing import List

from components import CompileResult


class Interface:
    def print_success(self, output: str) -> None:
        print("success:", output)

    def print_error(self, output: str) -> None:
        print("error:", output)

    def print_output(self, compile_result: CompileResult) -> None:
        if compile_result.success: self.print_success(compile_result.output)
        else: self.print_error(compile_result.output)

    def print_progress(
        self, all_exercises: List[str], completed_exercises: List[str]
    ) -> None:
        progress = []
        progress.extend(["#" for _ in completed_exercises])
        if len(completed_exercises) < len(all_exercises):
            progress.append(">")
            progress.extend(
                ["-" for _ in all_exercises[len(completed_exercises) + 1 :]]
            )
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
