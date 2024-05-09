# dictionaries4.py

# Finsih the code below that loops through my_dict and add all the names (keys) to the names
# list and the phonenumbers (values) to the phonenumbers list.
# You can do this without extra methods, but feel free to check out the items method, to see if it
# is useful.

### I AM NOT DONE

my_dict = {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}

names = []
phonenumbers = []

for x in my_dict:
    pass

# Don't modify code below
# Feel free to look at it and understand what the keys and values methods do.

if names != list(my_dict.keys()):
    raise ValueError("names are supposed to be", list(my_dict.keys()))

if phonenumbers != list(my_dict.values()):
    raise ValueError("phonenumbers are supposed to be", list(my_dict.values()))