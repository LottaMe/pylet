import os
import subprocess
from typing import List

from components import Colors


class Interface:
    def __init__(self) -> None:
        self.colors = Colors()
        self.all_length = 0
        self.completed_length = 0

    def print_success(self, output: str = "") -> None:
        """
        Takes output string.
        Prints colorful success message, empty line and output.
        """
        print(
            self.colors.success,
            "Running the code was successful!",
            self.colors.standard,
        )
        print()
        print(output)

    def print_error(self, output: str) -> None:
        """
        Takes output string.
        Prints colorful error message, empty line and output.
        """
        print(
            self.colors.error,
            "Running the code failed! Please try again. Here's the output:",
            self.colors.standard,
        )
        print()
        print(output)

    def print_progress(self) -> None:
        """
        Uses attributes all_length and comleted_length.
        Prints colorful progress bar with:
            - # (success color) for successful exercises
            - > (neutral color) for current exercise
            - - (error color) for not started exercise
            - how many exercises are completed from total, and percent
        """
        progress = [self.colors.success]
        progress.extend(["#" for _ in range(self.completed_length)])
        if self.completed_length < self.all_length:
            progress.append(f"{self.colors.neutral}>{self.colors.error}")
            progress.extend(
                ["-" for _ in range(self.all_length - self.completed_length)]
            )
        progress.append(self.colors.standard)
        print(
            "progress:",
            "".join(progress),
            f"{self.completed_length}/{self.all_length}",
            f"{round(((self.completed_length / self.all_length) * 100),1)}%",
        )

    def print_course_complete(self) -> None:
        """
        Prints course completed message
        """
        print("You have completed the course!")

    def clear(self) -> None:
        """
        Runs terminal command "clear".
        """
        subprocess.run(["clear"])

    def create_folder(self, path: str) -> None:
        try:
            os.makedirs(path)
        except OSError as e:
            print(e)

    def create_file(self, path: str, content: str = "") -> None:
        with open(path, "x") as f:
            f.write(content)

    def create_summary_file(self, path: str):
        completed = [
            f"- [{f}](./completed/{f})" for f in os.listdir(f"{path}/completed")
        ]
        current = next(f"- [{f}](./{f})" for f in os.listdir(path) if ".py" in f)
        progress = f"{self.completed_length}/{self.all_length} ({round((self.completed_length/self.all_length)*100, 2)}%)"

        summary = [
            f"## PROGRESS: {progress}",
            "",
            "### current: ",
            "",
            current,
            "",
            "### completed: ",
            "",
        ]
        summary.extend(sorted(completed))
        summary.append("")
        with open(f"{path}/summary.md", "x") as f:
            f.write("\n".join(summary))

    def print_summary_error(self) -> None:
        print(self.colors.error)
        print("Please remove the ./summary folder to generate a new summary.")
        print(self.colors.standard)

    def create_summary_folder(
            self, 
            completed_exercises: list, 
            current_exercise
        ) -> None:
        try:
            self.create_folder("./summary")
            self.create_folder("./summary/completed")

            current_name = current_exercise.path.split("/")[-1]
            self.create_file(f"./summary/{current_name}", current_exercise.code_str)

            for exercise in completed_exercises:
                name = exercise.path.split("/")[-1]
                self.create_file(f"./summary/completed/{name}", exercise.code_str)

            self.create_summary_file("./summary")
        except FileExistsError:
            self.print_summary_error()