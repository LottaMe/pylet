import os
import subprocess
import zipfile
from typing import TYPE_CHECKING, Dict, List

from components import Colors

if TYPE_CHECKING:
    from exercise import Exercise


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
            "\n Remove the # I AM NOT DONE comment to continue",
            self.colors.standard,
        )
        print()
        print(output)

    def print_failure(self, output: str, test: bool = False) -> None:
        """
        Takes output string and test boolean.
        Prints colorful failure message for running or testing the code, empty line and output.
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
        print("Congratsss!! You have completed the courssssse!")
        print(
            r"""
                      __    __    __    __
                     /  \  /  \  /  \  /  \
____________________/  __\/  __\/  __\/  __\_____________________________
___________________/  /__/  /__/  /__/  /________________________________
                   | / \   / \   / \   / \  \____
                   |/   \_/   \_/   \_/   \    o \
                                           \_____/--<
              """
        )

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
            f.write(content.encode())

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

        self.create_file_in_zip(archive, f"{path}/summary.md", "\n".join(summary))

    def create_summary_zip(
        self, completed_exercises: List["Exercise"], current_exercise: "Exercise"
    ) -> None:
        """
        Take lists of exercises and the current exercise and create a zip file summary with
        completed exercises, current exercises and summary file.
        """
        with zipfile.ZipFile("summary.zip", mode="w") as archive:

            self.create_file_in_zip(
                archive,
                f"./summary/{current_exercise.name}.py",
                current_exercise.code_str,
            )

            for exercise in completed_exercises:
                self.create_file_in_zip(
                    archive,
                    f"./summary/completed/{exercise.name}.py",
                    exercise.code_str,
                )

            self.create_summary_file_in_zip(archive, "./summary")

    def get_order_index(self, exercises: List[str]) -> str:
        """
        Take list of exercises, display them numbered to the user and ask for them to
        pick an index. If the index is valid, return it.
        """
        self.clear()
        for i, exercise in enumerate(exercises):
            print(f"{i}. {exercise}")
        user_input = input("pick first exercise or exercise group    ")
        if user_input not in [str(f) for f in range(len(exercises))]:
            user_input = self.get_order_index(exercises)
        return user_input

    def order_exercises(self, exercise_paths: List[str]) -> List[str]:
        """
        Take list of exercise_paths and order them with the help of user input.
        For folders, add all python files in folder to ordered list.
        Return ordered list.
        """
        exercise_order = []

        while len(exercise_paths) > 0:
            user_input = self.get_order_index(exercise_paths)

            if os.path.isdir(f"exercises/{exercise_paths[int(user_input)]}"):
                for exercise in [
                    f
                    for f in sorted(
                        os.listdir(f"exercises/{exercise_paths[int(user_input)]}")
                    )
                    if ".py" in f
                ]:
                    exercise_order.append(
                        f"{exercise_paths[int(user_input)]}/{exercise}"
                    )
            else:
                exercise_order.append(exercise_paths[int(user_input)])
            # remove picked item
            exercise_paths.pop(int(user_input))

        return exercise_order

    def create_exercise_info_yaml(self, exercises: Dict[str, str]) -> None:
        yaml_list = ["exercises:"]
        for exercise in exercises:
            yaml_list.append(
                f"""  {exercise["name"]}:
    path: {exercise["path"]}
    test: {exercise["test"]}"""
            )
        yaml_list.append("")
        with open("exercise_info.yaml", "x") as f:
            f.write("\n".join(yaml_list))
