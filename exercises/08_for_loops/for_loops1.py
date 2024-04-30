# for_loops1.py

# We have the list from list1.
# We want to loop through it with a for loop, print the ingredient,
# and add it to ingredientsABC if it starts with a, b or c.
# Hint: you can access a position in a string the same way that you can access it in lists

### I AM NOT DONE

ingredients = ["beans", "teriyaki sauce", "apricot jam", "plum jam", "coconut milk"]
ingredientsABC = []

for ingredient in ingredients:
    print(ingredient)


# Don't modify code below


if ingredientsABC !=  ["beans", "apricot jam", "coconut milk"]:
    raise ValueError("You need to add ingredients that start with a, b, or c to ingredientsABC")
else:
    print("ingredientsABC:", ingredientsABC)