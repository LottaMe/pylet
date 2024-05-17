import threading
from unittest.mock import MagicMock
from interface import Interface
from exercise import Exercise
from runner import Runner


def write_in_file(path, content):
    with open(path, "w") as f:
        f.write(content)


def safe_old_content(path):
    with open(path, "r") as f:
        return f.read()


def test_pylet(capsys):
    interface = Interface()
    runner = Runner(
        exercise_info_path="./pylet/e2e/exercise_info.yaml", interface=interface
    )
    exercises = runner.get_exercises()
    assert exercises[0].path == "exercises/exercise1.py"
    assert exercises[0].test == False

    # change exercise paths
    for exercise in exercises:
        new_path = "./pylet/e2e/" + exercise.path
        exercise.path = new_path

    # check path is correct
    assert exercises[0].path == "./pylet/e2e/exercises/exercise1.py"

    # fix returnvalue of get_exercises to use new paths
    runner.get_exercises = MagicMock(return_value=exercises)

    # run exercise1
    old_content1 = safe_old_content(exercises[0].path)
    old_content2 = safe_old_content(exercises[1].path)
    old_content3 = safe_old_content(exercises[2].path)
    old_content4 = safe_old_content(exercises[3].path)

    run_thread = threading.Thread(target=runner.run)
    run_thread.start()

    # change exercise1 - one change - tests false
    goal_content1 = """
# exercise1.py


# Make the code print a greeting to the world.


print ("hello world!")
"""
    write_thread1 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[0].path,
            goal_content1,
        ),
    )
    write_thread1.start()
    write_thread1.join()

    # change exercise2 - one change - tests true
    goal_content2 = """
# exercise2.py


# Write function that adds 1


def add_one(number):
    return number + 1


def test_add_one():
    assert add_one(1) == 2
    assert add_one(-1) == 0
    assert add_one(12) == 13

"""
    write_thread2 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[1].path,
            goal_content2,
        ),
    )
    write_thread2.start()
    write_thread2.join()

    # change exercise3 - multiple changes - tests false
    part1_goal_content3 = """
# exercise3.py


# Make the code print a greeting to the world.

### I AM NOT DONE

print("hello world!")
"""
    part2_goal_content3 = """
# exercise3.py


# Make the code print a greeting to the world.

### I AM NOT DONE

print("hello steve!")
"""
    goal_content3 = """
# exercise3.py


# Make the code print a greeting to the world.


print("hello steve!")
"""
    write_thread3 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[2].path,
            part1_goal_content3,
        ),
    )
    write_thread3.start()
    write_thread3.join()

    write_thread3 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[2].path,
            part2_goal_content3,
        ),
    )
    write_thread3.start()
    write_thread3.join()

    write_thread3 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[2].path,
            goal_content3,
        ),
    )
    write_thread3.start()
    write_thread3.join()

    # change exercise4 - one change - infinite while loop - tests false
    goal_content4 = """
# exercise4.py


# Make the code print a greeting to the world.

counter = 0
while counter < 1:
    print("counter is", counter)
    counter += 1
"""
    write_thread4 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[3].path,
            goal_content4,
        ),
    )
    write_thread4.start()
    write_thread4.join()

    # change exercise5 - one change - import packages - tests false
    goal_content5 = """
# exercise5.py


# Import packages

import random
import math
import time

random.randint(0, 2)
math.pi
time.time()
"""
    write_thread5 = threading.Thread(
        target=write_in_file,
        args=(
            exercises[4].path,
            goal_content5,
        ),
    )
    write_thread5.start()
    write_thread5.join()

    # finish run and add asserts
    run_thread.join()

    captured = capsys.readouterr()

    assert "You have completed the course!" in captured.out

    # revert exercises
    write_in_file(exercises[0].path, old_content1)
    write_in_file(exercises[1].path, old_content2)
    write_in_file(exercises[2].path, old_content3)
    write_in_file(exercises[3].path, old_content4)
