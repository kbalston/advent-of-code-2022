#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Optional


class Program:
    def __init__(self) -> None:
        self.x = 1
        self.signalStrength = 0
        self.signalStrengthCycle = 40
        self.signalStrengthCycleOffset = 20
        self.pixels: list[str] = list()
        self.cycle = 1

    def recordSignalStrength(self) -> None:
        if (
            self.cycle % self.signalStrengthCycle
            == self.signalStrengthCycleOffset
        ):
            thisSignalStrength = self.x * self.cycle
            self.signalStrength += thisSignalStrength
            self.trace(
                f"recordSignalStrength of {thisSignalStrength}"
            )

    def trace(self, str: str) -> None:
        print(f"[{self.cycle:3}] [x={self.x:3}] {str}")

    def recordPixel(self) -> None:
        horiz = (self.cycle - 1) % 40
        spritePos = (self.x - 1, self.x, self.x + 1)
        if horiz in spritePos:
            c = "#"
        else:
            c = "."
        self.pixels.append(c)
        if self.cycle % 40 == 0:
            self.pixels.append("\n")
        self.trace(
            f"Pixels with new='{c}'; horiz={horiz}; x={self.x}"
        )
        print("".join(self.pixels))
        self.trace("/Pixels")

    def advanceCycle(self, cycleCost: int) -> None:
        assert (
            self.signalStrengthCycle > self.signalStrengthCycleOffset
        )
        for _ in range(cycleCost):
            self.recordPixel()
            self.recordSignalStrength()
            self.cycle += 1

    def addx(self, value: int) -> None:
        self.trace(f"Begin addx {value}")
        self.advanceCycle(1)
        self.advanceCycle(1)
        self.x += value
        self.trace(f"Execute addx {value}")

    def noop(self) -> None:
        self.trace("Begin noop")
        cycleCost = 1
        self.advanceCycle(cycleCost)
        self.trace("Execute noop")


def solve(
    lines: list[str],
    expectedPattern: Optional[str],
    sumOfSignalStrengths: int,
) -> None:
    program = Program()

    # Read in data
    for lineFull in lines:
        line = lineFull.split()
        cmd = line[0]
        if cmd == "addx":
            value = int(line[1])
        else:
            value = None

        match cmd:
            case "addx":
                assert value is not None
                program.addx(value)
            case "noop":
                program.noop()
            case _:
                assert False

    print(f"Calculated: {program.signalStrength}")
    print(f"=> Expecting {sumOfSignalStrengths}")
    assert program.signalStrength == sumOfSignalStrengths

    if expectedPattern:
        calculated = "".join(program.pixels)

        print("Checking pattern...")
        for i, (p1, p2) in enumerate(
            zip(calculated, expectedPattern)
        ):
            assert (
                p1 == p2
            ), f"Index {i} does not match: '{p1}' != '{p2}'"
        print("=> Matches expected pattern:")
        print(expectedPattern)


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open(
    "day10-input-trivial.txt", "r", encoding="utf-8"
) as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    expectedPattern=None,
    sumOfSignalStrengths=0,
)

with open("day10-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    expectedPattern=None,
    sumOfSignalStrengths=13140,
)

with open("day10-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    expectedPattern=None,
    sumOfSignalStrengths=17940,
)

# Part 2
expectedPattern = (
    "##..##..##..##..##..##..##..##..##..##..\n"
    "###...###...###...###...###...###...###.\n"
    "####....####....####....####....####....\n"
    "#####.....#####.....#####.....#####.....\n"
    "######......######......######......####\n"
    "#######.......#######.......#######....."
)
with open("day10-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    expectedPattern=expectedPattern,
    sumOfSignalStrengths=13140,
)

expectedPattern = (
    "####..##..###...##....##.####...##.####.\n"
    "...#.#..#.#..#.#..#....#.#.......#....#.\n"
    "..#..#....###..#..#....#.###.....#...#..\n"
    ".#...#....#..#.####....#.#.......#..#...\n"
    "#....#..#.#..#.#..#.#..#.#....#..#.#....\n"
    "####..##..###..#..#..##..#.....##..####."
)
with open("day10-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    expectedPattern=expectedPattern,
    sumOfSignalStrengths=17940,
)
