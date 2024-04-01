import os
import subprocess
import time
from typing import List
import yaml
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer
from interface import Interface


class CompileResult:
    def __init__(self, success: bool, output: str) -> None:
        self.success = success
        self.output = output


class ExerciseHandler:
    def __init__(self, path: str, interface: Interface) -> None:
        self.path = path
        self.interface = interface
        self.exercises = self.get_exercises(path)

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

    def watch_exercise_till_pass(self, path) -> None:
        event_handler = FileSystemEventHandler()
        # event_handler.on_modified
        observer = Observer()
        observer.schedule(event_handler, path, recursive=True)
        observer.start()

        try:
            while self.compile_exercise(path=path).success != True:
                time.sleep(1)
            else:
                observer.stop()
                observer.join()
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
            if compile_result.success == True:
                self.interface.print_success(compile_result.output)
            else:
                self.interface.print_error(compile_result.output)
                # exit = ""
                # valid_exits = ["exit", "exit()", "q"]
                self.watch_exercise_till_pass(path=exercise_path)
