# classes2.py

# We are writing a class that models a dog.
# Finish writing the bark and the sit method.
# Can you use the dog attribute name in the methods?

### I AM NOT DONE

class Dog:
    def __init__(self, name: str, age: str) -> None:
        self.name = name
        self.age = age

    def bark(self) -> str:
        return
    
    def sit(self) -> str:
        return

doggo = Dog("doggo", 1)

print(doggo.bark())
print(doggo.sit())

# Don't modify code below

if not isinstance(doggo.bark(), str):
    raise ValueError("The bark method of Dog should return a string")

if not isinstance(doggo.sit(), str):
    raise ValueError("The sit method of Dog should return a string")