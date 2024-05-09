# error_handling2.py

# We have function raise_different_errors, that either raises a
# NameError or a ValueError. If the error_type is not name or value it raises no error
# and returns nothing.
# Please finish the function handle_error, that tries to execute the function
# and handles both the NameError and ValueError, by returning different error messages
# if there is no error, it should return the string "no error".

### I AM NOT DONE

# don't change this function
def raise_different_errors(error_type: str):
    if error_type == "name":
        raise NameError()
    elif error_type == "value":
        raise ValueError()
    
def handle_error(error_type: str):
    try:
        raise_different_errors(error_type)  # don't change this line
    


# Don't modify code below

def test_handle_error_output():
    assert isinstance(handle_error("name"), str)
    assert isinstance(handle_error("value"), str)

def test_handle_different_errors():
    assert handle_error("name") != handle_error("value")

def test_handle_else():
    assert handle_error("") == "no error"