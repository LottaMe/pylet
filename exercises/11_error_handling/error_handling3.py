# error_handling3.py

# We have a function maybe_raise_error that takes a boolean and if it is
# True raises an Error. Finish the handle_error function, so it returns a list outputs, 
# that either has a message "error", if maybe_raise_error threw an error, or the message
# "no error", if maybe_raise_error threw no error.
# in either case, it should add the message "bye bye :) and return the outputs list"

### I AM NOT DONE

# don't change this function
def maybe_raise_error(error: bool):
    if error:
        raise ValueError()
    
def handle_error(error: bool):
    outputs = []
    try:
        maybe_raise_error(error)  # don't change this line
    

# Don't modify code below
outputs = handle_error(True)
for output in outputs: 
    print(output)
assert outputs == ["error", "bye bye :)"]

outputs = handle_error(False)
for output in outputs: 
    print(output)
assert outputs == ["no error", "bye bye :)"]