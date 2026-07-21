# https://www.geeksforgeeks.org/python/adapter-method-python-design-patterns/

from abc import ABC

class Vehicle(ABC):
    def __init__(self, mass: int, max_speed: int):
        self.mass = mass
        self.max_speed = max_speed

    def drive(self):
        return f"driven at a max speed of {self.max_speed}"


class MotorCycle(Vehicle):
    """Class for MotorCycle"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "MotorCycle"

    def TwoWheeler(self):
        return "TwoWheeler"


class Truck(Vehicle):
    """Class for Truck"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Truck"

    def EightWheeler(self):
        return "EightWheeler"


class Car(Vehicle):
    """Class for Car"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "Car"

    def FourWheeler(self):
        return "FourWheeler"


class Adapter:
    """
    Adapts an object by replacing methods.
    Usage:
    motorCycle = MotorCycle()
    motorCycle = Adapter(motorCycle, wheels = motorCycle.TwoWheeler)
    """

    def __init__(self, obj, **adapted_methods):
        """We set the adapted methods in the object's dict"""
        self.obj = obj
        self.__dict__.update(adapted_methods)

    def __getattr__(self, attr):
        """All non-adapted calls are passed to the object"""
        return getattr(self.obj, attr)

    def original_dict(self):
        """Print original object dict"""
        return self.obj.__dict__


def train(adapter: Adapter):
    assert isinstance(adapter, Adapter), f"input is not of class Adapter"

    print(f"A {adapter.name} is a {adapter.wheels()} vehicle that is {adapter.drive()}")

# main method
if __name__ == "__main__":
    """list to store objects"""
    objects = []

    motorCycle = MotorCycle(mass=1, max_speed=1)
    objects.append(Adapter(motorCycle, wheels=motorCycle.TwoWheeler))

    truck = Truck(mass=3, max_speed=0.5)
    objects.append(Adapter(truck, wheels=truck.EightWheeler))

    car = Car(mass=2, max_speed=1)
    objects.append(Adapter(car, wheels=car.FourWheeler))

    for obj in objects:
        train(obj)