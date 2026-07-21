from __future__ import annotations

from enum import Enum
from typing import Union

from pydantic import BaseModel

# An example of clean code instead of gathering all movements in seperate classes.
class AnimalMovements(Enum):
    LAND = "walk"
    WATER = "swim"
    AIR = "fly"

# from typing import Protocol, runtime_checkable

# # An example as a refactor starting point
# @runtime_checkable # lets isinstance() work at runtime
# class Animal(Protocol):
#     def move(self) -> str: ...
#     def speak(self) -> str: ...

# Protocol with one speak() fixes both.
class Dog:
    def __init__(self):
        self.sound = "woof"

    def __repr__(self):
        return f"{type(self).__name__} that {self.move()}"

    def bark(self):
        return self.sound

    def move(self):
        return f"{AnimalMovements.LAND.value} forward"


class Cat:
    def __init__(self):
        self.sound = "meow"

    def __repr__(self):
        return f"{type(self).__name__} that {self.move()}"

    def meow(self):
        return self.sound

    def move(self):
        return f"{AnimalMovements.LAND.value} forward"


class Dolphin:
    def __init__(self):
        self.sound = "click"

    def __repr__(self):
        return f"{type(self).__name__} that {self.move()}"

    def communicate(self):
        return self.sound

    def move(self):
        return f"{AnimalMovements.WATER.value} forward"


# TODO: hand-edited every time an animal is added.
Animal = Union[Dog, Cat, Dolphin]


# TODO: Factory pattern
def create_animal(kind: str):
    if kind == "dog":
        return Dog()
    elif kind == "cat":
        return Cat()
    elif kind == "dolphin":
        return Dolphin()
    else:
        return None


# TODO: Dependency injection
class ConsoleLogger:
    def log(self, msg: str):
        print(f"[game] {msg}")


class Game(BaseModel):
    animal: Animal
    model_config = {"arbitrary_types_allowed": True}  # Animal isn't a pydantic model

    # TODO: ?? something here
    def _logger(self):
        return ConsoleLogger()

    # TODO: ?? something here
    def play(self):
        log = self._logger()

        if isinstance(self.animal, Dog):
            log.log(self.animal.bark())
        elif isinstance(self.animal, Cat):
            log.log(self.animal.meow())
        elif isinstance(self.animal, Dolphin):
            log.log(self.animal.communicate())
        else:
            log.log("...silence...")

        log.log(repr(self.animal))

    # TODO: Can use Protocol here?
    @staticmethod
    def looks_like_animal(obj) -> bool:
        has_move = hasattr(obj, "move")
        has_sound = (
            hasattr(obj, "bark")
            or hasattr(obj, "meow")
            or hasattr(obj, "communicate")
        )
        return has_move and has_sound


# TODO: Can make a registry instead of hardcoding types
def main():
    for kind in ["dog", "cat", "dolphin", "wombat"]:
        animal = create_animal(kind)
        if animal is None:
            print(f"don't know how to make a {kind}")
            continue
        if not Game.looks_like_animal(animal):
            print(f"{kind} doesn't look like an Animal")
            continue
        game = Game(animal=animal)
        game.play()


if __name__ == "__main__":
    main()