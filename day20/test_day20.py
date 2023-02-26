# type: ignore

import pytest

from .day20 import move, Number


@pytest.mark.parametrize(
    "input,targetNumber,expected",
    [
        ([1, 2, -3, 3, -2, 0, 4], 1, [2, 1, -3, 3, -2, 0, 4]),
        ([2, 1, -3, 3, -2, 0, 4], 2, [1, -3, 2, 3, -2, 0, 4]),
        ([1, -3, 2, 3, -2, 0, 4], -3, [1, 2, 3, -2, -3, 0, 4]),
        ([1, 2, 3, -2, -3, 0, 4], 3, [1, 2, -2, -3, 0, 3, 4]),
        ([1, 2, -2, -3, 0, 3, 4], -2, [1, 2, -3, 0, 3, 4, -2]),
        ([1, 2, -3, 0, 3, 4, -2], 0, [1, 2, -3, 0, 3, 4, -2]),
        ([1, 2, -3, 0, 3, 4, -2], 4, [1, 2, -3, 4, 0, 3, -2]),
    ],
)
def test_move(
    input: list[int], targetNumber: int, expected: list[int]
):
    inputN = [Number(n) for n in input]
    for n in inputN:
        if n.value == targetNumber:
            targetN = n
            break
    else:
        assert False
    move(inputN, targetN)
    for n, e in zip(inputN, expected):
        assert n.value == e


def test_noop():
    assert True
