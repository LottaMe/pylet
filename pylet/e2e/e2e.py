import os
import threading
from unittest.mock import MagicMock
import zipfile

from interface import Interface
from runner import Runner


def get_initial_content(exercise_index):
    match exercise_index:
        case 0:
            return """
# exercise1.py


# Make the code print a greeting to the world.

### I AM NOT DONE

print "hello world!")
""".lstrip()
        case 1:
            return """
# exercise2.py


# Write function that adds 1

### I AM NOT DONE


def add_one(number):
    return number


def test_add_one():
    assert add_one(1) == 2
    assert add_one(-1) == 0
    assert add_one(12) == 13
""".lstrip()
        case 2:
            return """
# exercise3.py


# Make the code print a greeting to the world.

### I AM NOT DONE

print "hello world!"
""".lstrip()
        case 3:
            return """
# exercise4.py


# Make the code print a greeting to the world.

### I AM NOT DONE

counter = 0
while counter < 1:
    print("counter is", counter)
""".lstrip()
        case 4:
            return """
# exercise5.py

### I AM NOT DONE

# Import packages

import random
import math
import time

random.randint(0, 2)
math.pi
time.time()
""".lstrip()


def write_in_file(path, content):
    with open(path, "w") as f:
        f.write(content)



def test_pylet_watch(capsys):
    interface = Interface()
    runner = Runner(
        exercise_info_path="./pylet/e2e/exercise_info.yaml", interface=interface
    )
    exercises = runner.get_exercises()

    # assert that get_exercises worked
    assert exercises[0].path == "exercises/exercise1.py"
    assert exercises[0].test == False

    for index, exercise in enumerate(exercises):
        # change exercise path to test path
        new_path = "./pylet/e2e/" + exercise.path
        exercise.path = new_path

        # change file content to initial content, in case it didn't reset
        write_in_file(new_path, get_initial_content(index))

    # check new path is correct
    assert exercises[0].path == "./pylet/e2e/exercises/exercise1.py"

    # have get_exercises return adjusted exercises
    runner.get_exercises = MagicMock(return_value=exercises)

    # start runner.run
    run_thread = threading.Thread(target=runner.watch)
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

    # finish run
    run_thread.join()

    # revert exercises
    write_in_file(exercises[0].path, get_initial_content(0))
    write_in_file(exercises[1].path, get_initial_content(1))
    write_in_file(exercises[2].path, get_initial_content(2))
    write_in_file(exercises[3].path, get_initial_content(3))
    write_in_file(exercises[4].path, get_initial_content(4))

    # assert course completed message has printed
    captured = capsys.readouterr()

    assert (
        "progress: \x1b[1;32m#####\x1b[0;0m 5/5 100.0%\nCongratsss!! You have completed the courssssse!" in captured.out
    )
    assert r"""
                      __    __    __    __
                     /  \  /  \  /  \  /  \
____________________/  __\/  __\/  __\/  __\_____________________________
___________________/  /__/  /__/  /__/  /________________________________
                   | / \   / \   / \   / \  \____
                   |/   \_/   \_/   \_/   \    o \
                                           \_____/--<""" in captured.out


def test_pylet_summary():
    interface = Interface()
    runner = Runner(
        exercise_info_path="./pylet/e2e/exercise_info.yaml", interface=interface
    )
    exercises = runner.get_exercises()

    # assert that get_exercises worked
    assert exercises[0].path == "exercises/exercise1.py"
    assert exercises[0].test == False

    for index, exercise in enumerate(exercises):
        # change exercise path to test path
        new_path = "./pylet/e2e/" + exercise.path
        exercise.path = new_path

        # change file content to initial content, in case it didn't reset
        write_in_file(new_path, get_initial_content(index))

    # check new path is correct
    assert exercises[0].path == "./pylet/e2e/exercises/exercise1.py"

    # have get_exercises return adjusted exercises
    runner.get_exercises = MagicMock(return_value=exercises)

    # fix exercise1
    content1 = """# exercise1.py


# Make the code print a greeting to the world.

print("hello world!")
"""
    write_in_file(exercises[0].path, content1)

    # fix exercise2
    content2 = """# exercise2.py


# Write function that adds 1


def add_one(number):
    return number+1


def test_add_one():
    assert add_one(1) == 2
    assert add_one(-1) == 0
    assert add_one(12) == 13
"""
    write_in_file(exercises[1].path, content2)

    runner.summary()

    # asserts
    with zipfile.ZipFile("summary.zip", mode="r") as archive:
        assert sorted(archive.namelist()) == sorted(
            [
                "./summary/exercise3.py",
                "./summary/completed/exercise1.py",
                "./summary/completed/exercise2.py",
                "./summary/summary.md",
            ]
        )
        assert archive.read("./summary/exercise3.py") == exercises[2].code_str.encode()
        assert archive.read("./summary/completed/exercise1.py") == content1.encode()
        assert archive.read("./summary/completed/exercise2.py") == content2.encode()
        assert archive.read("./summary/summary.md") == """## PROGRESS: 2/5 (40.0%)

### current: 

- [exercise3.py](./exercise3.py)

### completed: 

- [exercise1.py](./completed/exercise1.py)
- [exercise2.py](./completed/exercise2.py)
""".encode()

    write_in_file(exercises[0].path, get_initial_content(0))
    write_in_file(exercises[1].path, get_initial_content(1))

    os.remove("./summary.zip")
    
