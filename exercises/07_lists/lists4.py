# lists4.py

# Change the lists on the right side of the assert statements,
# so that they pass.
# Consider how the different methods to remove items from lists work.

### I AM NOT DONE

remove_example = ["apple", "banana", "pear", "banana"]
assert remove_example.remove("banana") == ["apple", "banana", "pear", "banana"]

pop_example_1 = ["apple", "banana", "pear", "banana"]
assert pop_example_1.pop() == ["apple", "banana", "pear", "banana"]

pop_example_2 = ["apple", "banana", "pear", "banana"]
assert pop_example_2.pop(0) == ["apple", "banana", "pear", "banana"]

clear_example = ["apple", "banana", "pear", "banana"]
assert clear_example.clear() == ["apple", "banana", "pear", "banana"]

del_example_1 = ["apple", "banana", "pear", "banana"]
del del_example_1[0] 
assert del_example_1 == ["apple", "banana", "pear", "banana"]

del_example_2 = ["apple", "banana", "pear", "banana"]
del del_example_2   # Note that this deletes the entire list. del_example_2 does not exist anymore
