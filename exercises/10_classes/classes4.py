# classes4.py

# We have created a few classes.
# An Animal class, that takes in the animals name and what kind of animal it is,
# a FarmAnimal class, that inherits from Animal and can use the work and the describe method,
# a Pet class, that inherits from Animal and can use the pet and describe method,
# and a Horse class, that inherits from FarmAnimal and Pet, and should be able to use the work, pet 
# and describe method.

# The Horse class is inheriting the describe method from FarmAnimal and Pet.
# We want it to inherit the method from Pet, so it is described as cuddly rather then hardworking.
# Can you fix the Horse class, so it uses the correct describe method?


### I AM NOT DONE


class Animal:
    def __init__(self, name: str, animal_kind: str) -> None:
        self.name = name
        self.animal_kind = animal_kind


class FarmAnimal(Animal):
    def __init__(self, name: str, animal_kind: str) -> None:
        super().__init__(name, animal_kind)

    def work(self):
        return f"{self.name} is hard at work"

    def describe(self):
        return f"{self.name} is a hardworking {self.animal_kind}"


class Pet(Animal):
    def __init__(self, name: str, animal_kind: str) -> None:
        super().__init__(name, animal_kind)

    def pet(self):
        return f"You've pet {self.name}"

    def describe(self):
        return f"{self.name} is a cuddly {self.animal_kind}"


class Horse(FarmAnimal, Pet):
    def __init__(self, name: str) -> None:
        super().__init__(name, "horse")


sabrina = Horse("Sabrina")

print(sabrina.work())
print(sabrina.pet())
print(sabrina.describe())

# Don't modify code below

if sabrina.work() != "Sabrina is hard at work":
    raise ValueError("Sabrina should be hard at work")

if sabrina.pet() != "You've pet Sabrina":
    raise ValueError("You should be able to pet Sabrina")

if sabrina.describe() != "Sabrina is a cuddly horse":
    raise ValueError("Sabrina is more cuddly then hardworking")
