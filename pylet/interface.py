import subprocess

from components import Colors, Result


class Interface:
    def __init__(self) -> None:
        self.colors = Colors()
        self.all_length = 0
        self.completed_length = 0

    def print_success(self, output: str = "", test: bool = False) -> None:
        """
        Takes output string and test boolean.
        Prints colorful success message for running or testing the code, empty line and output.
        """
        message = "Running the code was successful!"
        if test:
            message = "Tests ran successfully!"
        print(
            self.colors.success,
            message,
            self.colors.standard,
        )
        print()
        print(output)

    def print_error(self, output: str, test: bool = False) -> None:
        """
        Takes output string and test boolean.
        Prints colorful error message for running or testing the code, empty line and output.
        """
        message = "Running the code failed! Please try again. Here's the output:"
        if test:
            message = "Tests failed! Please try again. Here's the output:"
        print(
            self.colors.error,
            message,
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
            progress.extend(["-" for _ in range(self.all_length - self.completed_length)])
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
