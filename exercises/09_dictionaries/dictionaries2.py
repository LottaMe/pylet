# dictionaries2.py

# We have created a dictionary for a person and the outline of a function "have_birthday".
# First, figure out what is wrong with our dictionary: hanna and fix it.
# Then, finish the function have_birthday. 
# It is supposed to take a dictionary, add 1 to the value of the key "age", and return the updated 
# dictionary.

### I AM NOT DONE

hanna = {
    "name": "Hanna",
    "name": "Miller",
    "age": 17,              # don't change this line
    "hobbies": ["reading", "gaming", "singing"]
}    

def have_birthday(person: dict) -> dict:
    return person


# Don't modify code below

hanna = have_birthday(hanna)

if hanna["age"] < 18:
    ValueError("Hanna isn't old enough!")