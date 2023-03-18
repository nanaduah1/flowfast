from dataclasses import dataclass
from typing import Callable, Generic, TypeVar
from flowfast.step import Step

I = TypeVar("I")
O = TypeVar("O")
T = TypeVar("T")


@dataclass
class _StepConnector(Step[I, O]):
    process_func: Callable[[I], O]

    def process(self, input: I) -> O:
        return self.process_func(input)


@dataclass
class Workflow(Generic[I, O]):
    step: Step[I, O]

    def next(self, next_step: Step[O, T]) -> "Workflow[I, T]":
        return Workflow(
            _StepConnector(lambda i: next_step.process(self.step.process(i)))
        )

    def run(self, input: I) -> O:
        return self.step.process(input)
