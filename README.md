# pylet 🐍🤍

Greetingsss. Welcome to `pylet`, the hands-on way to learn python.

It is encouraged to do your own research while using `pylet`. Here are some sources recommended by us:

- [python docs tutorial](https://docs.python.org/3/tutorial/index.html)
- [w3school python tutorial](https://www.w3schools.com/python/)

## Prerequisites

To use `pylet`, you need to have python3 installed.
You can look up how to download python [here](https://www.python.org/downloads/).

## First Setup

First create a virtual environment for the project, activate it and install the requirements:

```
python3 -m venv env
source env/bin/activate
```

Now that you are in the environment, you should install the dependencies in the requirements.tsx.

```
pip install -r requirements.txt
```

Now the requirements are installed in the virtual environment env.

In the future don't forget to activate the virtual environment before running the program with. If it is not active, the program won't run.

```
source env/bin/activate
```

## Run pylet

To run pylet enter:

```
python pylet
```

## Test the application

To test the application enter:

```
pytest
```

## Keep code formatting consistent

I am using black to keep the code formatting consistent.
The exercise folder should be excluded from formatting.
To do this run:

```
black . --extend-exclude exercises
isort pylet
```
