# functions4.py


# We have written a function count_missishippi that is supposed to 
# print the value of count and missishippi(s) and then increase count every time
# the function is called.
# count is a global variable
# Our code does not work. Can you fix it?
# Hint: you can either look into changing global variables, or make use of parameters, 
# local scope and reassigning variables to solve this exercise.

### I AM NOT DONE

count = 1

def count_missishippi() -> None:
    print(str(count), "missishippi(s)")
    count += 1

count_missishippi()
count_missishippi()


# # Don't modify code below

if(count<=1):
    raise ValueError("count should be increased when function is called")
