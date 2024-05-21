import argparse
from interface import Interface
from runner import Runner

if __name__ == "__main__":
    interface = Interface()

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--command", required=False, type=str)
    args = parser.parse_args()

    if args.command:
        print(args.command)
        exit(0)

    runner = Runner(exercise_info_path="exercise_info.yaml", interface=interface)

    runner.run()
