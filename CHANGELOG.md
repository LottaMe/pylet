# CHANGELOG

This file will for now include bigger changes in pylet, once it is open source, it will include changes to exercises as well. For now, it is mostly for changes and decisions on the pylet source code.
This will be written with the newest changes at the top, but I will create a few links to jump to specific sections:

- [Subprocess, compile/exec and multiprocessing](#subprocess-compileexec-and-multiprocessing)
  - [First Solution - Subprocess](#first-solution---subprocess)
  - [First Major Change - compile & exec](#first-major-change---compile--exec)
  - [Introducing: Multiprocessing](#introducing-multiprocessing)
- [1.0.0 Adding Queue](#100-adding-queue)

## 1.0.0 Adding Queue

There was a percistent bug after introducing multiprocessing, that is explained in [this issue](https://github.com/LottaMe/pylet/issues/44).

This bug was fixed, by introducing another feature of the multiprocessing package -> Queue.
We are adding a boolean to the queue that gives informaion about whether to move on to the next exercise.
It is set every time the exercise.run function is called and is gotten from the queue whenever the queue is not empty in the runner.run function.

## Subprocess, compile/exec and multiprocessing

### First Solution - Subprocess

The first solution was using subprocess to take the path to the exercise, run subprocess with python and the path

```python
subprocess(['python', path], capture_output=True, text=True)
```

This will execute the python program and capture either the output or the error message if the program does not successfully execute.

This worked well until I started implementing exercises with while loops.

With subprocess the entire file will execute before you get the entire output. With while loops, just from an asthetic point of view, we want to see the program execute line by line.

More importantly: It is very easy for beginners to write infinite while loops. The program will never finish executing and we will never get the output.

Now, we could solve this with a timeout in the subprocess function, but this showed another problem:

Watchdog, which is used to watch for file changes and then restart the subprocess, does not work concurrently with the subprocess. It is waiting for the subprocess to finish to keep watching for file changes. This is again not good when we are handling loops, as you want to be able to interrupt the execution of a loop when you change the file.

### First Major Change - compile & exec

This brings us to the first major change. Instead of using subprocess, we are using the python internal functions `compile` and `exec`.

First we are using `compile` to check for any SyntaxErrors it can catch. If there are none, we are trying to execute the file with `exec`.

This solved the aesthetic problem, as we now saw the output of programs as they were running, instead of only seeing it as it completed.

It did not fix the problem of watchdog waiting for the program execution to finish.

## Introducing: Multiprocessing

To fix the watchdog issue, I introduced `multiprocessing`.

With multiprocessing, you can start a new process that will execute a task. It runs parallel to the main process, on which watchdog keeps watching for file changes.

So now that we are executing the exercise code and at the same time watching for file changes.

This is not a perfect solution, so here are some of the problems:

- multiprocessing works different on different operating systems, so it might be buggy on e.g. windows
- multiprocessing is a big abstraction for low level processes at work. It is hard to use in python, because of that level of abstraction
