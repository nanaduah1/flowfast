import pytest
from dataclasses import dataclass
from flowfast.step import Step
from flowfast.workflow import Workflow


@dataclass
class AddFactor(Step[int, int]):
    factor: int

    def process(self, input: int) -> int:
        print("Shitting: ", self.factor)
        return input + self.factor


def test_empty_workflow_errors():
    with pytest.raises(TypeError):
        Workflow()


def test_one_step_workflow():
    tested = Workflow(AddFactor(1))
    actual = tested.run(1)
    expected = 2

    assert actual == expected


def test_2_step_workflow():
    tested = Workflow(AddFactor(1)).next(AddFactor(2))
    actual = tested.run(1)
    expected = 4

    assert actual == expected


def test_3_step_workflow():
    tested = (
        Workflow(AddFactor(1))  # Add 1 to input
        .next(AddFactor(2))  # add 2 to input
        .next(AddFactor(3))  # add 3 to input
        .next(AddFactor(-3))  # Subtract 3 from input
    )
    actual = tested.run(0)
    expected = 3

    assert actual == expected


def test_iterable_input_flow():
    wf = Workflow(AddFactor(1))
    tested = Workflow.for_each(wf)
    expected = [2, 1, 5]

    actual = tested.run([1, 0, 4])
    assert actual == expected
