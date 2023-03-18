from abc import ABC, abstractmethod
from typing import Generic, TypeVar

I = TypeVar("I")
O = TypeVar("O")
T = TypeVar("T")


class WorkflowBase(ABC, Generic[I, O]):
    @abstractmethod
    def run(self, input: I):
        pass


class Step(ABC, Generic[I, O]):
    @abstractmethod
    def process(self, input: I) -> O:
        pass
