import argparse
from interface import Interface
from runner import Runner

def watch(args):
    interface = Interface()
    runner = Runner(exercise_info_path="exercise_info.yaml", interface=interface)

    runner.run()

def summary(args):
    print("summary not implemented yet")

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

watch_parser = subparsers.add_parser("watch")
watch_parser.set_defaults(func=watch)

summary_parser = subparsers.add_parser("summary")
summary_parser.set_defaults(func=summary)

if __name__ == "__main__":
    args = parser.parse_args()
    args.func(args)  # call the default function
