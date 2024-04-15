# functions5.py


# You are writing code to calculate the final price
# to charge on items on an online shop.
# You are give the item price, you should add a 10% tax
# and then give the buyer a 5% discount.
# The results should always be rounded to 2 places.
# We have started writing the functions for you.
# Can you finish them?


### I AM NOT DONE

def calculate_final_price(price: float) -> float:
    price_with_tax = add_tax(price)
    final_price = add_discount(price_with_tax)
    return final_price

def add_tax(price: float) -> float:
    return

def add_discount(price: float) -> float:
    return


# Don't modify code below

def test_add_tax():
    assert add_tax(100) == 110.0
    assert add_tax(3) == 3.3

def test_add_discount():
    assert add_discount(100) == 95.0
    assert add_discount(3) == 2.85

def test_calculate_final_price():
    assert calculate_final_price(100) == 104.5
    assert calculate_final_price(3) == 3.13
