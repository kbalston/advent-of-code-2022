#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Tuple


class RopeEnd:
    def __init__(self, name: str, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        self.name = name

    def __repr__(self) -> str:
        return f"{self.name}{{{self.x},{self.y}}}"

    def move(self, xRel: int, yRel: int) -> None:
        self.x += xRel
        self.y += yRel
        print(f"=> Moved  {xRel}, {yRel} to {self}")

    def updateTail(self, head: RopeEnd) -> None:
        # self is tail
        while True:
            xDist = head.x - self.x
            yDist = head.y - self.y
            print(f"==> xDist={xDist}; yDist={yDist}")
            if abs(xDist) >= 2:
                xChange = +1 if xDist > 0 else -1
                if yDist != 0:
                    yChange = +1 if yDist > 0 else -1
                else:
                    yChange = 0
            elif abs(yDist) >= 2:
                if xDist != 0:
                    xChange = +1 if xDist > 0 else -1
                else:
                    xChange = 0
                yChange = +1 if yDist > 0 else -1
            else:
                break
            print(f"===> Moving {xChange}, {yChange}")
            self.move(xChange, yChange)


class Rope:
    def __init__(self, numberOfKnots: int) -> None:
        assert numberOfKnots >= 2
        self.knots = [
            RopeEnd(f"Knot{i}") for i in range(numberOfKnots)
        ]
        self.head = self.knots[0]
        self.tailHistory: set[Tuple[int, int]] = set()

    def __repr__(self) -> str:
        return f"Rope{{{self.knots}}}"

    def move(self, xRel: int, yRel: int) -> None:
        print(f"=> Moving {xRel}, {yRel}")
        self.head.move(xRel, yRel)
        for i, knot in enumerate(self.knots[1:]):
            knot.updateTail(self.knots[i])
        self.tailHistory.add((self.knots[-1].x, self.knots[-1].y))
        print(f"==> {self}\n")


def solve(
    lines: list[str], numberOfKnots: int, solution: int
) -> None:
    rope = Rope(numberOfKnots)
    for line in lines:
        direction, countStr = line.split()
        count = int(countStr)
        print(
            f"\nMoving {count} in direction {direction} from {rope}"
        )
        for _ in range(count):
            match direction:
                case "L":
                    rope.move(-1, 0)
                case "R":
                    rope.move(+1, 0)
                case "U":
                    rope.move(0, +1)
                case "D":
                    rope.move(0, -1)
                case _:
                    assert False

    # Part 1
    visitedLocations = len(rope.tailHistory)
    print(f"Tail has visited {visitedLocations} locations")
    print(f"=> Expecting {solution} locations")
    assert visitedLocations == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day9-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, numberOfKnots=2, solution=13)

with open("day9-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, numberOfKnots=2, solution=6354)

# Part 2
with open("day9-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, numberOfKnots=10, solution=1)

with open(
    "day9-input-test-part-2.txt", "r", encoding="utf-8"
) as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, numberOfKnots=10, solution=36)

with open("day9-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, numberOfKnots=10, solution=2651)
