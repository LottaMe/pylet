# functions4.py


# We have written a function count_missishippi that is supposed to 
# print a number and missishippi(s) and then increase that number every time
# the function is called.
# Our logic is flawed. Can you fix it?


### I AM NOT DONE

count = 1

def count_missishippi(count: int) -> None:
    print(str(count), "missishippi(s)")
    count += count

count_missishippi(count)
count_missishippi(count)


# # Don't modify code below

if(count<=1):
    raise ValueError("count should be increased when function is called")
