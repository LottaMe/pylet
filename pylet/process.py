import multiprocessing as mp


class PyletProcess(mp.Process):
    def __init__(self, exercise, queue: mp.Queue) -> None:
        super().__init__()
        self.exercise = exercise
        self.queue = queue

    def run(self) -> None:
        self.queue.put({"wait": True})
        self.exercise.run(self.queue)
