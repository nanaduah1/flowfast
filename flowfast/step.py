from abc import ABC, abstractmethod
from typing import TypeVar, Generic

I = TypeVar("I")
O = TypeVar("O")


class Step(ABC, Generic[I, O]):
    @abstractmethod
    def process(self, input: I) -> O:
        pass
