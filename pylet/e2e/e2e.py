from unittest.mock import MagicMock
from interface import Interface
from exercise import Exercise
from runner import Runner


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
    
    runner.run()