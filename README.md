# pylet 🐍🤍

Greetingsss. Welcome to `pylet`, the hands-on way to learn python.

It is encouraged to do your own research while using `pylet`. Here are some sources recommended by us:

- [python docs tutorial](https://docs.python.org/3/tutorial/index.html)
- [w3school python tutorial](https://www.w3schools.com/python/)

## Prerequisites

To use `pylet`, you need to have python3 installed.
You can look up how to download python [here](https://www.python.org/downloads/).

## Getting Started

_This is a very early version of `pylet` and currently only tested on mac._

### Manually

#### Get Repository

First you need to get the repository locally.
You can either clone the repository:

```
git clone git@github.com:LottaMe/pylet.git
```

Or you download the repository as a .zip and unpack it locally.

#### Create virtual environment

When you have the repository, open a terminal in the root folder of the repository.

First you need to create a virtual environment for the project. You do this with this command in the terminal:

```
python3 -m venv env
```

Next, enter the virtual environment:

```
source env/bin/activate
```

Now that you are in the environment, you should install the dependencies in the requirements.tsx.

```
pip install -r requirements.txt
```

Now the requirements are installed in the virtual environment env and you are ready to start with the exercises

## Run `pylet`

Before running pylet, be sure that you are in the created virtual environment. You should see a little (env) at the left side of your terminal.

If you are not in the environment, the following command will simply fail.

You can enter the environment with this command:

```
source env/bin/activate
```

To run pylet enter:

```
python pylet
```

You can always exit it, with a KeyboardInterrupt (control + c).

As this is an early version, `pylet` may hang at times. Try exiting it and running pylet again.
