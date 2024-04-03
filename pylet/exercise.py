import os
import subprocess
import time
from functools import partial
from typing import List

import yaml
from interface import Interface
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output


class ExerciseHandler:
    def __init__(self, path: str, interface: Interface) -> None:
        self.path = path
        self.interface = interface
        self.exercises = self.get_exercises(path)
        self.completed_exercises = []

    def get_exercises(self, path) -> List[str]:
        with open(path) as f:
            exercises = yaml.safe_load(f)
        return exercises["exercises"]

    def check_file_exists(self, path) -> bool:
        return os.path.isfile(path)

    def compile_exercise(self, path) -> CompileResult:
        result = subprocess.run(["python", path], capture_output=True, text=True)
        if result.returncode == 0:
            return CompileResult(True, result.stdout)
        else:
            return CompileResult(False, result.stderr)

    def test_exercise(self, path) -> CompileResult:
        result = subprocess.run(["pytest", path], capture_output=True, text=True)
        return CompileResult(True, result.stdout)
        
    def check_done_comment(self, path: str) -> bool:
        with open(path, "r") as f:
            lines = f.readlines()
            for line in lines:
                if line.find("# I AM NOT DONE") != -1:
                    return True
        return False

    def on_modified(self, event, path):
        self.interface.clear()
        result = self.compile_exercise(path)
        if result.success == True:
            self.interface.print_success(result.output)
            test = self.test_exercise(path)
            self.interface.print_success(test.output)
        else:
            self.interface.print_error(result.output)

    def wait_on_exercise(self, path) -> bool:
        result = self.compile_exercise(path=path)
        if not result.success:
            return True
        if result.success and self.check_done_comment(path=path):
            return True
        return False

    def watch_exercise_till_pass(self, path) -> None:
        event_handler = FileSystemEventHandler()
        event_handler.on_modified = partial(self.on_modified, path=path)
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while self.wait_on_exercise(path=path):
                time.sleep(1)
            else:
                observer.stop()
                observer.join()
                self.completed_exercises.append(path)
        except KeyboardInterrupt:
            observer.stop()
            observer.join()
            exit(0)

    def run(self) -> None:
        for exercise in self.exercises:
            exercise_path = f"exercises/{exercise}.py"
            if not self.check_file_exists(exercise_path):
                continue
            compile_result = self.compile_exercise(exercise_path)
            self.test_exercise(exercise_path)

            if compile_result.success == True:
                if self.check_done_comment(path=exercise_path):
                    self.interface.clear()
                    self.interface.print_progress(self.exercises, self.completed_exercises)
                    self.interface.print_success(compile_result.output)

                    self.watch_exercise_till_pass(path=exercise_path)
                else:
                    continue

            else:
                self.interface.clear()
                self.interface.print_progress(self.exercises, self.completed_exercises)
                self.interface.print_error(compile_result.output)

                self.watch_exercise_till_pass(path=exercise_path)
        
        self.interface.print_progress(self.exercises, self.completed_exercises)
        self.interface.print_course_complete()
