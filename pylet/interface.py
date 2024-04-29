import subprocess
from typing import List

from components import Colors, Result


class Interface:
    def __init__(self) -> None:
        self.colors = Colors()
        self.all_length = 0
        self.completed_length = 0

    def print_success(self, output: str = "") -> None:
        print(
            self.colors.success,
            "Running the code was successful!",
            self.colors.standard,
        )
        print()
        print(output)

    def print_error(self, output: str) -> None:
        print(
            self.colors.error,
            "Running the code failed! Please try again. Here's the output:",
            self.colors.standard,
        )
        print()
        print(output)

    def print_output(self, result: Result) -> None:
        if result.success:
            self.print_success(result.output)
        else:
            self.print_error(result.output)

    def print_progress(self, all_length: int, completed_length: int) -> None:
        progress = [self.colors.success]
        progress.extend(["#" for _ in range(completed_length)])
        if completed_length < all_length:
            progress.append(f"{self.colors.neutral}>{self.colors.error}")
            progress.extend(["-" for _ in range(all_length - completed_length)])
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
