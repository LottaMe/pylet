import subprocess

from components import Colors, Result


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

    def handle_command_inputs(self, hint_message: str = "No hint for this exercise") -> None:
        """
        Open the standard input to get user input.
        If the result includes 'hint', print out hint_message.
        """
        try:
            with open(0) as stdin:
                result = stdin.readline()
                if "hint" in result:
                    print(hint_message)
        except OSError:
            print("command failed")
