from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Iterable, List, Tuple

from flowfast.base import Step, WorkflowBase

Mapping = Dict[str, Any]
Predicate = Callable[[Mapping], bool]


class Task(Step[Mapping, Mapping]):
    pass


@dataclass
class _Condition:
    predicate: Predicate
    step: Step

    def eval(self, input: Mapping) -> Tuple[bool, Step]:
        predicate_result = self.predicate(input)
        if predicate_result is True:
            return (True, self.step)
        return (False, None)


@dataclass
class Choice(Task):
    _choices: List[_Condition] = field(default_factory=list)

    def process(self, input: Mapping) -> Mapping:
        for condition in self._choices:
            matched, step = condition.eval(input)
            if matched is True:
                return step.process(input)

        return input

    def when(self, predicate: Predicate, step: Step):
        self._choices.append(_Condition(predicate, step))
        return self
