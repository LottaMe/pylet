import threading
from unittest.mock import MagicMock
from interface import Interface
from exercise import Exercise
from runner import Runner

def write_in_file():
    with open("./pylet/e2e/exercises/exercise1.py", "w") as f:
        f.write("""
# intro2.py


# Make the code print a greeting to the world.


print ("hello world!")
""")
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

    run_thread = threading.Thread(target=runner.run)
    # runner.run()
    write_thread = threading.Thread(target=write_in_file)
    run_thread.start()
    write_thread.start()
    run_thread.join()
    write_thread.join()
    