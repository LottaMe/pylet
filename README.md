# pylet

A tool to learn python that is inspired by rustlings.

## First Setup

First create a virtual environment for the project, activate it and install the requirements:

```
python3 -m venv env
source env/bin/activate
```

Now that you are in the environment, you can use the make commands defined in the Makefile.

```
run setup
```

Now the requirements are installed in the virtual environment env.

In the future don't forget to activate the virtual environment before running the program with. If it is not active, the program won't run.

```
source env/bin/activate
```

## Run pylet

To run pylet enter:

```
make run
```

## Test the application

To test the application enter:

```
make test
```

## Keep code formatting consistent

I am using black to keep the code formatting consistent.
The exercise folder should be excluded from formatting.
To do this run:

```
make format
```
