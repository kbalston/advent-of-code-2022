#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Optional

from rich import print  # type: ignore


class Program:
    def __init__(self) -> None:
        self.cycle = 1
        self.x = 1
        self.signalStrength = 0
        self.signalStrengthCycle = 40
        self.signalStrengthCycleOffset = 20

    def recordSignalStrength(self) -> None:
        thisSignalStrength = self.x * self.cycle
        self.signalStrength += thisSignalStrength
        print(
            f"[{self.cycle:3}] recordSignalStrength of"
            f" {thisSignalStrength}"
        )

    def advanceCycle(self, cycleCost: int) -> None:
        assert (
            self.signalStrengthCycle > self.signalStrengthCycleOffset
        )
        for i in range(cycleCost):
            self.cycle += 1
            if (
                self.cycle % self.signalStrengthCycle
                == self.signalStrengthCycleOffset
            ):
                self.recordSignalStrength()

    def addx(self, value: int) -> None:
        print(f"[{self.cycle:3}] addx {value}")
        self.advanceCycle(1)
        self.x += value
        self.advanceCycle(1)

    def noop(self) -> None:
        print(f"[{self.cycle:3}] noop")
        cycleCost = 1
        self.advanceCycle(cycleCost)


class Number:
    def __init__(self, value: str, decryptionKey: int = 1) -> None:
        self.value = int(value) * decryptionKey

    def __repr__(self) -> str:
        return f"{self.value}"


def move(numbers: list[Number], numberToMove: Number) -> None:
    previousIndex = numbers.index(numberToMove)
    numbers.pop(previousIndex)
    newIndex = (previousIndex + numberToMove.value) % len(numbers)
    if newIndex == 0:
        newIndex = len(numbers)
    numbers.insert(newIndex, numberToMove)


def solve(
    lines: list[str],
    times: int = 1,
    decryptionKey: int = 1,
    solution: Optional[int] = None,
) -> None:
    input = list()
    zero = None
    # Read in data
    for line in lines:
        n = Number(line, decryptionKey)
        input.append(n)
        if line == "0":
            zero = n
    assert zero is not None

    initialInput = input[:]
    for _ in range(times):
        for n in initialInput:
            move(input, n)

    print(f"Final is {input}")
    zi = input.index(zero)
    print(f"Zero is at index {zi}")

    s = 0
    for x in (1000, 2000, 3000):
        v = input[(zi + x) % (len(input) - 0)]
        s += v.value
        print(f"{x} is {v}")
    print(s)

    print(f"Calculated:  {s}")
    print(f"=> Expecting {solution}")
    assert s == solution


if __name__ == "__main__":
    os.chdir(os.path.realpath(os.path.dirname(__file__)))

    # Part 1
    with open(
        "day20-input-test.txt", "r", encoding="utf-8"
    ) as inputFile:
        lines = inputFile.read().splitlines()
    solve(
        lines,
        solution=3,
    )

    with open("day20-input.txt", "r", encoding="utf-8") as inputFile:
        lines = inputFile.read().splitlines()
    solve(
        lines,
        solution=10831,
    )

    # Part 2
    with open(
        "day20-input-test.txt", "r", encoding="utf-8"
    ) as inputFile:
        lines = inputFile.read().splitlines()
    solve(
        lines,
        times=10,
        decryptionKey=811589153,
        solution=1623178306,
    )

    with open("day20-input.txt", "r", encoding="utf-8") as inputFile:
        lines = inputFile.read().splitlines()
    solve(
        lines,
        times=10,
        decryptionKey=811589153,
        solution=6420481789383,
    )
