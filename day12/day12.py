#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import List, Optional, Tuple


class Position:
    def __init__(
        self, y: int, x: int, elevation: str, allowAnyStart: bool
    ) -> None:
        self.x = x
        self.y = y
        if elevation == "S":
            elevation = "a"
            self.start = True
        elif allowAnyStart and elevation == "a":
            self.start = True
        else:
            self.start = False
        self.score: Optional[int]
        if elevation == "E":
            elevation = "z"
            self.end = True
            self.score = 0
        else:
            self.end = False
            self.score = None
        self.elevation = ord(elevation) - ord("a")

    def __repr__(self) -> str:
        scoreStr = self.score if self.score is not None else "?"
        return f"Position{{{self.y},{self.x}@{self.elevation}={scoreStr}}}"


class Grid:
    def __init__(self, height: int, width: int) -> None:
        self.height = height
        self.width = width
        # Lets preallocate the full table
        initialValue: Optional[Position] = None
        self.grid = [[initialValue] * width for _ in range(height)]
        self.start: Optional[Position] = None
        self.end: Optional[Position] = None

    def add(
        self, y: int, x: int, elevation: str, allowAnyStart: bool
    ) -> None:
        pos = Position(
            y=y, x=x, elevation=elevation, allowAnyStart=allowAnyStart
        )
        self.grid[y][x] = pos
        if elevation == "E":
            self.end = pos

    def getEnd(self) -> Position:
        assert self.end
        return self.end

    def getPos(self, y: int, x: int) -> Position:
        p = self.grid[y][x]
        assert p is not None
        return p

    def isInsideBounds(self, coord: Tuple[int, int]) -> bool:
        y = coord[0]
        x = coord[1]
        if y < 0 or y >= self.height or x < 0 or x >= self.width:
            print(f"=> isInsideBounds -> {y},{x} is outside bounds")
            return False
        else:
            return True

    def isClimbable(
        self, dest: Position, sourceY: int, sourceX: int
    ) -> bool:
        source = self.getPos(y=sourceY, x=sourceX)
        if dest.elevation <= source.elevation + 1:
            print(f"==> Can    climb from {source} to {dest}")
            return True
        else:
            print(f"==> CANNOT climb from {source} to {dest}")
            return False

    def getAdjacentAndClimbable(
        self, pos: Position
    ) -> List[Position]:
        allCoordinates = (
            (pos.y - 1, pos.x + 0),
            (pos.y + 1, pos.x + 0),
            (pos.y + 0, pos.x - 1),
            (pos.y + 0, pos.x + 1),
        )
        validCoordinates = list(
            filter(self.isInsideBounds, allCoordinates)
        )
        climbableCoord = []
        for coordinate in validCoordinates:
            climbable = self.isClimbable(
                dest=pos, sourceY=coordinate[0], sourceX=coordinate[1]
            )
            if climbable:
                climbableCoord.append(
                    self.getPos(y=coordinate[0], x=coordinate[1])
                )

        return climbableCoord

    def astar(self) -> Position:
        opens = [self.getEnd()]
        opensNext = []

        while opens:
            print(f"\nNext iteration: {opens}")
            for dest in opens[:]:
                print(f"{dest}: Considering adjacencies")
                assert dest.score is not None
                sources = self.getAdjacentAndClimbable(dest)
                for source in sources:
                    print(f"=> Can climb from {dest} to {source}")
                    thisScore = dest.score + 1
                    if (
                        source.score is None
                        or source.score > thisScore
                    ):
                        source.score = thisScore
                        opensNext.append(source)
                    if source.start:
                        print("Found start!")
                        return source
            opens = opensNext[:]
            opensNext = []

        assert False, "Did not find a path from E to S"


def solve(lines: list[str], part2: bool, solution: int) -> None:
    height = len(lines)
    width = len(lines[0])
    grid = Grid(height=height, width=width)

    for y, line in enumerate(lines):
        for x, pos in enumerate(line):
            print(f"[{y}],[{x}]->{pos}")
            grid.add(y=y, x=x, elevation=pos, allowAnyStart=part2)

    found = grid.astar()
    print(found)
    if solution is not None:
        assert found.score == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day12-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part2=False, solution=31)

with open("day12-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part2=False, solution=383)

# Part 2
with open("day12-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part2=True, solution=29)

with open("day12-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part2=True, solution=377)
