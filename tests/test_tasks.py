from dataclasses import dataclass, field
from flowfast.step import Choice, _Condition, Task


@dataclass
class FakeStep(Task):
    name: str = "fake_calls"

    def process(self, input: dict) -> dict:
        calls = input.get(self.name, 0)
        return {**input, self.name: calls + 1}


def test_truth_condition():
    step = FakeStep()
    tested = _Condition(
        predicate=lambda i: i.get("ok") is True,
        step=step,
    )

    matched, out_step = tested.eval({"ok": True})

    assert matched is True
    assert out_step == step


def test_false_condition():
    step = FakeStep()
    tested = _Condition(
        predicate=lambda i: i.get("ok") is False,
        step=step,
    )

    matched, out_step = tested.eval({"ok": True})

    assert matched is False
    assert out_step is None


def test_2_choice_step():
    tested = Choice()
    step_a = FakeStep()

    tested.when(lambda i: i.get("ok") is True, step_a)

    output = tested.process({"ok": True})

    assert "fake_calls" in output
    assert output["fake_calls"] == 1


def test_single_choice_step():
    tested = Choice()
    step_a = FakeStep(name="step_a")
    step_b = FakeStep(name="step_b")

    tested.when(lambda i: i.get("step_a") is True, step_a)
    tested.when(lambda i: i.get("age") <= 10, step_b)

    output = tested.process({"age": 9})

    assert step_a.name not in output
    assert step_b.name in output

    assert output[step_b.name] == 1


def test_no_matching_choice_step():
    tested = Choice()
    step_a = FakeStep()

    tested.when(lambda i: i.get("ok") is True, step_a)

    output = tested.process({"ok": False})

    assert step_a.name not in output
