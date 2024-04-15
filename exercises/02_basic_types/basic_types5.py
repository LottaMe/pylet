# basic_types5.py


# Fix the code, so that it compiles.
# The results are supposed to be strings, not integers or floats
# Hint: Just like a int() and float() function, there is a str() function


### I AM NOT DONE

turn_me_into_string = 6

plus_66 = turn_me_into_string + "66"

times_3 = turn_me_into_string * 3


print(turn_me_into_string, "plus 66 is", plus_66)
print(turn_me_into_string, "times 3 is", times_3)

# Don't modify code below

if not isinstance(plus_66, str):
    raise TypeError("plus_66 is supposed to be a string.")

if not isinstance(times_3, str):
    raise TypeError("times_3 is supposed to be a string.")

