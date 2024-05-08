# standard_library1.py

# Let's explore some parts of pythons standard library, starting with a package 
# you have seen before. time.
# We started writing a program that runs a function and prints out the time it took to 
# run that function. 
# Can you finish the code for us?

### I AM NOT DONE

import time

# don't change this function
def some_function():
    print("running function")
    time.sleep(0.5)


start = time.time()

some_function()

end =
runtime = 

print("program ran for...", runtime)

# Don't modify code below

if end < start:
    raise ValueError("end should be bigger than start")

if runtime != end - start:
    raise ValueError("runtime should be the difference between end and start")
