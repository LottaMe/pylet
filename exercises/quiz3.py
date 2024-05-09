# quiz3.py

# We are implementing three shapes as classes. Rectangle, Square and Circle.
# For each of them, implement an area method, that calculates the area and a to_dict method
# to return a dictionary of the objects attributes and their area. You can take a look at the tests 
# for a better idea what the implementation should return.
# Please round your area calculations to 2 places after the decimal point.

### I AM NOT DONE


import math


class Rectangle:
    def __init__(self, width: int | float, length: int | float) -> None:
        pass
    def area(self) -> int | float:
        pass

    def to_dict(self) -> dict:
        pass

class Square(Rectangle):
    def __init__(self, width: int | float) -> None:
        super().__init__()

class Circle:
    def __init__(self, radius: int | float) -> None:
        pass
    def area(self) -> int | float:
        pass

    def to_dict(self) -> dict:
        pass


# Don't modify code below
def test_rectangle_area():
    example_rectangle1 = Rectangle(2, 4)
    assert example_rectangle1.area() == 8

    example_rectangle1 = Rectangle(2.4, 3.7)
    assert example_rectangle1.area() == 8.88

def test_rectangle_dict():
    example_rectangle1 = Rectangle(2, 4)
    assert example_rectangle1.to_dict() == {
        "width": 2,
        "length": 4,
        "area": 8
    }

    example_rectangle2 = Rectangle(2.4, 3.7)
    assert example_rectangle2.to_dict() == {
        "width": 2.4,
        "length": 3.7,
        "area": 8.88
    }
def test_square_area():
    example_square1 = Square(3)
    assert example_square1.area() == 9

    example_square2 = Square(1.5)
    assert example_square2.area() == 2.25


def test_square_dict():
    example_square1 = Square(3)
    assert example_square1.to_dict() == {
        "width": 3,
        "length": 3,
        "area": 9
    }
    example_square2 = Square(1.5)
    assert example_square2.to_dict() == {
        "width": 1.5,
        "length": 1.5,
        "area": 2.25
    }

def test_circle_area():
    example_circle1 = Circle(3)
    assert example_circle1.area() == 28.27

    example_circle2 = Circle(1.5)
    assert example_circle2.area() == 7.07

def test_circle_dict():
    example_circle1 = Circle(3)
    assert example_circle1.to_dict() == {
        "radius": 3,
        "area": 28.27
    }

    example_circle2 = Circle(1.5)
    assert example_circle2.to_dict() == {
        "radius": 1.5,
        "area": 7.07
    }