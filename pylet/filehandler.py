from process import PyletProcess
from watchdog.events import FileSystemEvent, FileSystemEventHandler


class FileChangeHandler(FileSystemEventHandler):
    def __init__(self, exercise, process):
        super().__init__()
        self.exercise = exercise
        self.process = process

    def on_modified(self, event: FileSystemEvent) -> None:
        print("File modified, restarting...")
        if self.process and self.process.is_alive():
            self.process.terminate()
            self.process.join()
        self.process = PyletProcess(self.exercise)
        self.process.start()
        self.process.join()
