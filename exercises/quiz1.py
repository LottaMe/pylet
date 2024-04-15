# quiz1.py


# Calculate final price of buying a number of friendship bracelets.

# One bracelet is 3 euros
# If you buy 5+, its only 2 euro per bracelet
# If you buy 15+, its only 1 euro per bracelet
# If you are 60+, you also get a 10 percent discount

# Write function that takes in amount of bracelets that you buy 
# and age of the customer and returns the final price.
# You can write everything in the calculate_final_price function, or seperate logic out
# to other functions, as long as calculate_final_price returns the final price.


## I AM NOT DONE

def calculate_final_price(amount: int, age: int) -> float | int:
    return



# Don't modify code below


def test_calculate_final_price_no_discount():
    assert calculate_final_price(4, 19) == 12
    assert calculate_final_price(6, 19) == 12
    assert calculate_final_price(20, 19) == 20

def test_calculate_final_price_with_discount():
    assert calculate_final_price(4, 65) == 10.8
    assert calculate_final_price(6, 65) == 10.8
    assert calculate_final_price(20, 65) == 18.0

def test_calculate_final_price_edge_cases():
    assert calculate_final_price(5, 19) == 10
    assert calculate_final_price(15, 19) == 15
    assert calculate_final_price(4, 60) == 10.8
    assert calculate_final_price(15, 60) == 13.5
