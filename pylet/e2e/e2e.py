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
    runner = Runner(exercise_info_path="./pylet/e2e/exercise_info.yaml", interface=interface)
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
    
    run_thread = threading.Thread(target=runner.run)
    run_thread.start()

    # change exercise1 - one change - tests false
    goal_content1 = """
# exercise1.py


# Make the code print a greeting to the world.


print ("hello world!")
"""
    write_thread1 = threading.Thread(target=write_in_file, args=(exercises[0].path, goal_content1,))
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
    write_thread2 = threading.Thread(target=write_in_file, args=(exercises[1].path, goal_content2,))
    write_thread2.start()
    write_thread2.join()

    run_thread.join()

    captured = capsys.readouterr()

    assert "You have completed the course!" in captured.out
    # revert exercises
    write_in_file(exercises[0].path, old_content1)
    write_in_file(exercises[1].path, old_content2)

    