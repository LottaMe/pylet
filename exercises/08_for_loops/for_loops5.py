# for_loops5.py

# Something in python that is adjacent to for_loops and lists is
# list comprehension.
# List comprehension offers a shorter syntax when you want 
# to create a new list based on the values of an existing list.
# We have written a list comprehension for you, that is creating a list from
# every number in number_list times 2.
# Can you create power_two, a list that is every item from number_list to the power
# of two with list comprehension?

### I AM NOT DONE

number_list = [1, 2, 3, 4, 5]
print("number_list:", number_list)

times_two = [num*2 for num in number_list]
print("times_two:", times_two)

power_two = []
print("power_two:", power_two)


# Don't modify code below

if power_two != [1, 4, 9, 16, 25]:
    raise ValueError("power_two is not each item in number_list**2")