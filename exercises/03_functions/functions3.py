# functions3.py


# We tried to write a function format_name, that takes a firstname and a 
# lastname and returns a fullname, but we made a mistake.
# Can you fix it?


### I AM NOT DONE


def format_name(firstname: str, lastname: str) -> str:
    fullname = firstname + " " + lastname

print(fullname)

# Don't modify code below

def test_format_name():
    assert format_name("John Doe") == "John Doe"
    assert format_name("Max", "Mustermann") == "Max Mustermann"

