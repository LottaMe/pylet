# Contributing to pylet

Thanksss for wanting to contribute 🐍🤍!!

## Working on pylet code & adding a pylet feature

1. Create an Issue to discuss the changes
2. Get your idea approved & create a feature branch (on your issue, click on create branch, then check the branch out locally)
3. Work on the feature.
   - we are using [pytest for testing](#test-the-application)
   - Write unittests for your new code
   - Frequently run existing tests
   - Update existing tests if you update existing code
   - frequently run [black and isort](#keep-code-formatting-consistent)
   - finally, create a pull request and wait for someone to review it
   - Once approved, pull request will be merged
   - Congrats!! You have contributed 🤍🤍

## Adding/changing an Exercise

1. Create an Issue briefly explaining the exercise you want to add or change
2. Create a feature branch (on your issue, click on create branch, then check the branch out locally).
3. Create an exercise file
   - in the exercises folder, there are many subfolders sorted by topics. Either add the exercise to a fitting subfolder, or create a new subfolder.
4. Add the exercise to the [exercise_info.yaml](/exercise_info.yaml), following the following format.
   - path is the path to the exercise (without .py at the end)
   - test is a boolean. If you have tests in your exercise file, set it to true, otherwise it should be false

```yaml
<exercise_name>:
  path: <exercise_path>
  test: <boolean>
```

## Specific Devolement Guides

### Test the application

You should regularly run unittests, with:

```
pytest
```

Before creating a pull request you should also run the end to end test with:

```
pytest pylet/e2e/e2e.py -s # the -s flag is so you see the output while running the test
```

### Keep code formatting consistent

I am using black to keep the code formatting consistent.
The exercise folder should be excluded from formatting.
To do this run:

```
black pylet
isort pylet
```
