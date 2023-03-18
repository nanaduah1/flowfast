import pytest
from dataclasses import dataclass
from flowfast.step import Step
from flowfast.workflow import Workflow


@dataclass
class LoggerStep(Step[int, int]):
    factor: int

    def process(self, input: int) -> int:
        print("Shitting: ", self.factor)
        return input + self.factor


def test_empty_workflow_errors():
    with pytest.raises(TypeError):
        Workflow()


def test_one_step_workflow():
    tested = Workflow(LoggerStep(1))
    actual = tested.run(1)
    expected = 2

    assert actual == expected


def test_2_step_workflow():
    tested = Workflow(LoggerStep(1)).next(LoggerStep(2))
    actual = tested.run(1)
    expected = 4

    assert actual == expected


def test_3_step_workflow():
    tested = (
        Workflow(LoggerStep(1))
        .next(LoggerStep(2))
        .next(LoggerStep(3))
        .next(LoggerStep(3))
        .next(LoggerStep(-3))
        .next(LoggerStep(3))
        .next(LoggerStep(-3))
    )
    actual = tested.run(1)
    expected = 7

    assert actual == expected
