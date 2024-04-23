import multiprocessing as mp

class PyletProcess(mp.Process):
    def __init__(self, exercise) -> None:
        super().__init__()
        self.exercise = exercise

    def run(self) -> None:
        self.exercise.run()