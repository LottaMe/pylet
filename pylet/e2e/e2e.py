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
    
def test_pylet():
    interface = Interface()
    runner = Runner(exercise_info_path="./pylet/e2e/exercise_info.yaml", interface=interface)
    exercises = runner.get_exercises()
    assert exercises[0].path == "exercises/exercise1.py"
    assert exercises[0].test == False

    for exercise in exercises: 
        new_path = "./pylet/e2e/" + exercise.path
        exercise.path = new_path

    assert exercises[0].path == "./pylet/e2e/exercises/exercise1.py"
    
    runner.get_exercises = MagicMock(return_value=exercises)

    old_content = safe_old_content("./pylet/e2e/exercises/exercise1.py")
    goal_content = """
# exercise1.py


# Make the code print a greeting to the world.


print ("hello world!")
"""

    run_thread = threading.Thread(target=runner.run)
    write_thread = threading.Thread(target=write_in_file, args=("./pylet/e2e/exercises/exercise1.py", goal_content,))
    run_thread.start()
    write_thread.start()
    run_thread.join()
    write_thread.join()

    write_thread = write_in_file("./pylet/e2e/exercises/exercise1.py", old_content)

    