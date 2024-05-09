# dictionaries3.py

# Change the lists on the right side of the assert statements,
# so that they pass.
# Consider how the different methods to add or remove items from dictionaries work.

### I AM NOT DONE

contacts = {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}

add_example = contacts.copy()
add_example["Matty"] = "357-235-0486"
assert add_example == {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}

pop_example = contacts.copy()
pop_example.pop("Sam")
assert pop_example == {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}

del_example = contacts.copy()
del del_example["Sophia"]
assert del_example == {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}

clear_example = contacts.copy()
clear_example.clear()
assert clear_example == {
    "Chloe": "123-456-7890",
    "Sam": "124-876-7400",
    "Sophia": "135-098-8360",
    "Markus": "973-235-0835",
}
