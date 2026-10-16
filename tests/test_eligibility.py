import pytest

from src.eligibility import assess


def test_meets_criteria_at_the_boundaries():
    assert assess(50, "current", 1, 20).eligible
    assert assess(80, "former", 1, 20, years_since_quit=15).eligible


@pytest.mark.parametrize(
    "args",
    [
        (49, "current", 1, 30),  # too young
        (81, "current", 1, 30),  # too old
        (60, "current", 1, 19),  # 19 pack-years
        (60, "former", 1, 30, 16),  # quit too long ago
        (60, "never"),  # never smoked
    ],
)
def test_each_criterion_can_exclude(args):
    result = assess(*args)
    assert not result.eligible and result.reasons


def test_pack_years_and_multiple_reasons():
    r = assess(40, "current", 0.5, 10)
    assert r.pack_years == 5
    assert len(r.reasons) == 2  # age and pack-years
