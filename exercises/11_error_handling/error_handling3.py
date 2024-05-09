# error_handling3.py

# Our function handle_error tries to execute code
# that might throw an error.
# Finish the handle_error function, so it returns a list outputs, 
# that either has a message "error", if maybe_raise_error threw an error, or the message
# "no error", if maybe_raise_error threw no error.
# in either case, it should add the message "bye bye :) and return the outputs list"

### I AM NOT DONE

# don't change this function

    
def handle_error(error: bool):
    outputs = []
    try:
        # don't change this code block
        if error:
            raise ValueError()
    # your code here
    

# Don't modify code below
outputs = handle_error(True)
for output in outputs: 
    print(output)
assert outputs == ["error", "bye bye :)"]

outputs = handle_error(False)
for output in outputs: 
    print(output)
assert outputs == ["no error", "bye bye :)"]