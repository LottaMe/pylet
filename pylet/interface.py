import subprocess
import zipfile
from typing import TYPE_CHECKING, List

from components import Colors

if TYPE_CHECKING:
    from exercise import Exercise


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

    def create_file_in_zip(
        self, archive: zipfile.ZipFile, path: str, content: str = ""
    ) -> None:
        """
        In a ZipFile, create file at path, optionally with content.
        """
        with archive.open(path, "w") as f:
            f.write(content)

    def create_summary_file_in_zip(self, archive: zipfile.ZipFile, path: str):
        """
        In a ZipFile, create a summary file with progress information, a link to the current exercise
        and a list with links to the completed files.
        """
        zipfiles = archive.namelist()
        completed = [
            f"- [{f.split('/')[-1]}](./completed/{f.split('/')[-1]})"
            for f in zipfiles
            if "completed" in f
        ]
        current = next(
            f"- [{f.split('/')[-1]}](./{f.split('/')[-1]})"
            for f in zipfiles
            if "completed" not in f
        )
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

        self.create_file_in_zip(
            archive, f"{path}/summary.md", "\n".join(summary).encode()
        )

    def create_summary_zip(
        self, completed_exercises: List["Exercise"], current_exercise: "Exercise"
    ) -> None:
        """
        Take lists of exercises and the current exercise and create a zip file summary with
        completed exercises, current exercises and summary file.
        """
        with zipfile.ZipFile("summary.zip", mode="w") as archive:

            self.create_file_in_zip(
                archive, f"./summary/{current_exercise.name}.py", current_exercise.code_str.encode()
            )

            for exercise in completed_exercises:
                self.create_file_in_zip(
                    archive, f"./summary/completed/{exercise.name}.py", exercise.code_str.encode()
                )

            self.create_summary_file_in_zip(archive, "./summary")
