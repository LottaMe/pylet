import subprocess


class Interface:
    def print_success(self, output) -> None:
        print("success:", output)

    def print_error(self, output) -> None:
        print("error:", output)

    def print_progress(self) -> None:
        pass

    def print_course_complete(self) -> None:
        print("You have completed the course!")

    def clear(self) -> None:
        subprocess.run(["clear"])
