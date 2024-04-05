from interface import Interface
from runner import Runner

if __name__ == "__main__":
    interface = Interface()
    runner = Runner(exercise_info_path="exercise_info.yaml", interface=interface)

    runner.run()
