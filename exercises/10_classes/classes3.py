# classes3.py

# We have created a Pet class which is the parent class of the Dog 
# class (which is the child class).
# Dog is inheriting from pet, but we want you to make some changes:
# Please set animal_kind for the Dog class always to "dog", so that 
# it is not needed when initializing a Dog object.
# Then overwrite the speak method, so it is not returning the string
# "good morning to you", but something else, e.g. "bark bark bark"


### I AM NOT DONE

class Pet:
    def __init__(self, name: str, age: int, animal_kind: str) -> None:
        self.name = name
        self.age = age
        self.animal_kind = animal_kind

    def eat(self) -> str:
        return f"{self.name} is eating!!"
    
    def speak(self) -> str:
        return "good morning to you"
    
class Dog(Pet):
    def __init__(self, name: str, age: int) -> None:
        super().__init__(name, age, animal_kind)

    def speak(self) -> str:
        return super().speak()
    
doggo = Dog("doggo", 1)


# Don't modify code below

pet = Pet("", 2, "")
if doggo.speak() == pet.speak():
    raise ValueError("You should overwrite the speak function")

if doggo.animal_kind != "dog":
    raise ValueError("You should set the animal_kind attribute of dog objects to dog")
