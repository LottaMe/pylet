# for_loops4.py

# Write a function that takes a list,
# loops through it with a for loop, check if the item is
# the string "BREAK" and if it is, return the list until that 
# "BREAK statement".
# If the loop ends without having found a "BREAK",
# return the original list

### I AM NOT DONE

data_complete = [2, 5, 1, 0, 3, 4]

data_with_break = [4, 2, 0, "BREAK", 2]

def check_data_for_break(data: list) -> list:
    return


# Don't modify code below

def test_complete():
    data = [2, 5, 1, 0, 3, 4]
    assert check_data_for_break(data) == data

    data = [5, 3, 3, 4]
    assert check_data_for_break(data) == data

def test_with_break():
    data = [4, 2, 0, "BREAK", 2]
    assert check_data_for_break(data) == [4, 2, 0]

    data = [6, 9, "BREAK", 4, 2, 1]
    assert check_data_for_break(data) == [6, 9]

    