#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
import os
from collections import defaultdict
from typing import Sequence


@dataclass(frozen=True)
class Pos:
    y: int
    x: int

    def left(self) -> Pos:
        return Pos(self.y, self.x - 1)

    def right(self) -> Pos:
        return Pos(self.y, self.x + 1)

    def up(self) -> Pos:
        return Pos(self.y - 1, self.x)

    def down(self) -> Pos:
        return Pos(self.y + 1, self.x)

    def all(self) -> Sequence[Pos]:
        return tuple(
            (
                self.left(),
                self.right(),
                self.up(),
                self.down(),
                # Include wait
                self,
            )
        )


class Table:
    def __init__(self) -> None:
        self.map: defaultdict[Pos, list[str]] = defaultdict(list)
        self.maxX = 0
        self.maxY = 0
        self.positions = list()
        self.positions.append(Pos(y=0, x=1))

    def inBounds(self, pos: Pos) -> bool:
        if pos.x < 0 or pos.x > self.maxX:
            return False
        if pos.y < 0 or pos.y > self.maxY:
            return False
        return True

    def inWall(self, pos: Pos) -> bool:
        assert self.inBounds(pos)
        if pos.y == 0 and pos.x == 1:
            return False
        if pos.y == self.maxY and pos.x == self.maxX - 1:
            return False

        return (
            pos.y == 0
            or pos.y == self.maxY
            or pos.x == 0
            or pos.x == self.maxX
        )

    def wrapAroundWall(self, pos: Pos) -> Pos:
        assert self.inWall(pos)
        if pos.y == 0:
            pos = Pos(y=self.maxY - 1, x=pos.x)
        elif pos.y == self.maxY:
            pos = Pos(y=1, x=pos.x)
        elif pos.x == 0:
            pos = Pos(y=pos.y, x=self.maxX - 1)
        elif pos.x == self.maxX:
            pos = Pos(y=pos.y, x=1)
        else:
            assert False
        return pos

    def inBlizzardInNextStep(self, pos: Pos) -> bool:
        assert self.inBounds(pos)
        nextPos = self.get(pos)
        for c in ("<", ">", "^", "v"):
            if c in nextPos:
                return True
        else:
            return False

    def set(self, pos: Pos, value: str) -> None:
        prev = self.map[pos]
        currentLen = len(prev)
        assert currentLen == 0
        self.map[pos].append(value)
        if "#" == value:
            if pos.x > self.maxX:
                self.maxX = pos.x
            if pos.y > self.maxY:
                self.maxY = pos.y

    def append(self, pos: Pos, value: str) -> None:
        prev = self.map[pos]
        assert "#" not in prev
        self.map[pos].append(value)

    def get(self, pos: Pos) -> list[str]:
        targetData = self.map.get(pos, None)
        if targetData is None:
            return list(".")
        else:
            return targetData

    def sim(self) -> None:
        previous = self.map.copy()
        self.map.clear()
        # Do a first pass to set the walls
        for pos, vList in previous.items():
            for v in vList:
                if v == "#":
                    self.set(pos, v)
        # Find and move the blizzards
        for pos, vList in previous.items():
            nextPos = None
            for v in vList:
                match v:
                    case "#":
                        continue
                    case ".":
                        # Just drop the empty spots
                        continue
                    case ">":
                        nextPos = pos.right()
                    case "<":
                        nextPos = pos.left()
                    case "^":
                        nextPos = pos.up()
                    case "v":
                        nextPos = pos.down()
                    case _:
                        assert False
                if nextPos:
                    if self.inWall(nextPos):
                        nextPos2 = self.wrapAroundWall(nextPos)
                        nextPos = nextPos2
                    else:
                        pass
                    self.append(nextPos, v)


def solve(lines: list[str], trips: int, solutionMinutes: int) -> None:
    table = Table()
    for y, line in enumerate(lines, start=0):
        for x, v in enumerate(line, start=0):
            pos = Pos(y=y, x=x)
            if v != ".":
                table.set(pos, v)

    initialPos = Pos(y=0, x=1)
    finalPos = Pos(y=table.maxY, x=table.maxX - 1)
    targetPos = finalPos

    statesToCheck = set([initialPos])
    stage = 0
    for minute in range(1000):
        # Map should always reflect next blizzard state
        table.sim()
        statesToCheckNext = set()
        assert len(statesToCheck) > 0, "No states to check?"
        for thisPos in statesToCheck:
            for nextPos in thisPos.all():
                if not table.inBounds(nextPos):
                    continue
                if table.inWall(nextPos):
                    continue
                if table.inBlizzardInNextStep(nextPos):
                    continue
                statesToCheckNext.add(nextPos)
        if targetPos in statesToCheckNext:
            print(
                f"Got to {targetPos} at min {minute + 1};"
                f" stage={stage}"
            )
            statesToCheckNext.clear()
            statesToCheckNext.add(targetPos)
            stage += 1
            if targetPos == finalPos:
                targetPos = initialPos
            else:
                targetPos = finalPos
            if stage == trips:
                print(
                    "=> Found new best solution after"
                    f" {minute + 1} minutes"
                )
                print(
                    "=> Expecting                    "
                    f" {solutionMinutes} minutes"
                )
                assert minute + 1 == solutionMinutes
                return
        statesToCheck = statesToCheckNext


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day24-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionMinutes=18,
    trips=1,
)

with open("day24-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionMinutes=249,
    trips=1,
)

# Part 2
with open("day24-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionMinutes=54,
    trips=3,
)

with open("day24-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionMinutes=735,
    trips=3,
)
