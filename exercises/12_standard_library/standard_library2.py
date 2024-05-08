# standard_library2.py

# We've already tried out using basic math in python, but for some we need the math module.
# Write a function take_sqrt_if_not_infinite, that takes a number, checks if it is infinite, and if it isn't
# it is supposed to return the square root of that number.

### I AM NOT DONE

import math


def take_sqrt_if_not_infinite(number: int) -> float:
    return


numbers = [math.inf, 309, 3234, 3, 645, math.inf, 23]

for number in numbers:
    result = take_sqrt_if_not_infinite(number)

    if result:
        print(result)



    # Don't modify code below

    if not math.isinf(number) and take_sqrt_if_not_infinite(number) != math.sqrt(number):
        raise ValueError("Please reread description and fix your math")
