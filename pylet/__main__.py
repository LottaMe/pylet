import argparse
from interface import Interface
from runner import Runner

def summary():
    print("summary not implemented yet")

if __name__ == "__main__":
    interface = Interface()
    runner = Runner(exercise_info_path="exercise_info.yaml", interface=interface)

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    
    watch_parser = subparsers.add_parser("watch")
    watch_parser.set_defaults(func=runner.watch)

    summary_parser = subparsers.add_parser("summary")
    summary_parser.set_defaults(func=summary)

    args = parser.parse_args()
    args.func()  # call the default function
