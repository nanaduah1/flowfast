from dataclasses import dataclass
from typing import Callable, Iterable, TypeVar
from flowfast.base import WorkflowBase
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
class Workflow(WorkflowBase[I, O]):
    step: Step[I, O]

    def next(self, next_step: Step[O, T]) -> WorkflowBase[I, T]:
        return Workflow(
            _StepConnector(lambda i: next_step.process(self.step.process(i)))
        )

    def run(self, input: I) -> O:
        return self.step.process(input)

    @classmethod
    def for_each(cls, wf: WorkflowBase[I, O]) -> WorkflowBase[Iterable[I], Iterable[O]]:
        def _execute_all(inputs: Iterable[I]):
            results = []
            for input in inputs:
                results.append(wf.run(input))
            return results

        return Workflow[Iterable[I], Iterable[O]](_StepConnector(_execute_all))
