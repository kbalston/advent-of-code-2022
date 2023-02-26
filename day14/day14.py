#!/usr/bin/env python3

from __future__ import annotations

import os
from typing import Tuple


CHAR_SAND = "s"
CHAR_EMPTY = "."
CHAR_WALL = "#"
CHAR_VOID = "V"


def inc(
    currentPos: Tuple[int, int], endPos: Tuple[int, int]
) -> Tuple[int, int]:
    if currentPos[1] == endPos[1]:
        if currentPos[0] < endPos[0]:
            return (currentPos[0] + 1, currentPos[1])
        else:
            return (currentPos[0] - 1, currentPos[1])
    elif currentPos[0] == endPos[0]:
        if currentPos[1] < endPos[1]:
            return (currentPos[0], currentPos[1] + 1)
        else:
            return (currentPos[0], currentPos[1] - 1)
    else:
        assert False


def moveSand(
    grid: dict[Tuple[int, int], str], s: Tuple[int, int]
) -> Tuple[Tuple[int, int], bool, bool]:
    quiet = True

    down = (s[0], s[1] + 1)
    sDown = grid.get(down, CHAR_EMPTY)

    left = (s[0] - 1, s[1] + 1)
    sLeft = grid.get(left, CHAR_EMPTY)

    right = (s[0] + 1, s[1] + 1)
    sRight = grid.get(right, CHAR_EMPTY)

    # Attempt to move down
    if sDown in (CHAR_EMPTY, CHAR_VOID):
        # Empty, free to move
        if not quiet:
            print("==> Moving down")
        return down, True, sDown == CHAR_VOID
    # Attempt to move down and left
    elif sLeft in (CHAR_EMPTY, CHAR_VOID):
        # Empty, free to move
        if not quiet:
            print("==> Moving left")
        return left, True, sLeft == CHAR_VOID
    # Attempt to move down and right
    elif sRight in (CHAR_EMPTY, CHAR_VOID):
        # Empty, free to move
        if not quiet:
            print("==> Moving right")
        return right, True, sRight == CHAR_VOID
    else:
        return s, False, False


def countSand(grid: dict[Tuple[int, int], str]) -> int:
    sum = 0
    for pos, contents in grid.items():
        if contents == CHAR_SAND:
            print(f"Counted sand unit at {pos}")
            sum += 1
    visualize(grid)
    return sum


def visualize(grid: dict[Tuple[int, int], str]) -> None:
    minX = None
    maxX = None
    minY = 0
    maxY = None
    for (x, y), contents in grid.items():
        if contents == CHAR_SAND:
            if minX is None or x < minX:
                minX = x
            if maxX is None or x > maxX:
                maxX = x
            if maxY is None or y > maxY:
                maxY = y

    assert minX is not None
    assert maxX is not None
    assert maxY is not None
    for y in range(minY, maxY + 1 + 2):
        for x in range(minX - 2, maxX + 1 + 2):
            p = grid.get((x, y), CHAR_EMPTY)
            if (x, y) == (500, 0):
                p = "I"
            print(p, end="")
        print()
    print("Done printing")


def markGrid(
    grid: dict[Tuple[int, int], str],
    lastPos: Tuple[int, int],
    currentPos: Tuple[int, int],
    markAs: str = CHAR_WALL,
) -> None:
    print(f"markAsRock: {lastPos} to {currentPos}")
    while True:
        print(f"=> Marking {lastPos} as rock")
        grid[lastPos] = markAs
        if lastPos == currentPos:
            break
        lastPos = inc(lastPos, currentPos)


def solve(lines: list[str], part1: bool, solution: int) -> None:
    # Read in data
    grid: dict[Tuple[int, int], str] = {}
    for line in lines:
        print("#" * 20)
        print(line)
        lineSplit = line.split(" -> ")
        print(lineSplit)
        lineSplitMore = [
            tuple(component.split(",")) for component in lineSplit
        ]
        print(lineSplitMore)
        lineSplitMore2 = [
            (int(pos[0]), int(pos[1])) for pos in lineSplitMore
        ]
        lastPos = lineSplitMore2[0]
        for currentPos in lineSplitMore2[1:]:
            markGrid(grid, lastPos, currentPos)
            lastPos = currentPos

    minX = None
    maxX = None
    maxY = None
    for x, y in grid:
        if minX is None or x < minX:
            minX = x
        if maxX is None or x > maxX:
            maxX = x
        if maxY is None or y > maxY:
            maxY = y
    assert minX is not None
    assert maxX is not None
    assert maxY is not None

    xPad = 1000
    left = (minX - xPad, maxY + 2)
    right = (minX + xPad, maxY + 2)
    if part1:
        markAs = CHAR_VOID
    else:
        markAs = CHAR_WALL
    markGrid(grid, left, right, markAs=markAs)

    # Simulate
    sand = []
    sandInsertPos = (500, 0)
    quiet = True
    while True:
        print("#" * 20)
        # (Try to) add new sand
        if not quiet:
            print(f"Introducing new sand at {sandInsertPos}...")
        assert grid.get(sandInsertPos, None) != CHAR_SAND
        sand.append(sandInsertPos)
        grid[sandInsertPos] = CHAR_SAND
        # Simulate sand
        print("Simulating cycle...")
        hasMoved = False
        while sand:
            nextSand = []
            for s in sand:
                nextS, moved, abyss = moveSand(grid, s)
                if abyss:
                    grid[s] = CHAR_EMPTY
                    calculated = countSand(grid)
                    print(f"Counted {calculated} units of sand")
                    if solution:
                        print(f"=> Expecting {solution}")
                        assert calculated == solution
                    return
                elif moved:
                    if not quiet:
                        print(f"Sand moved from {s} to {nextS}")
                    grid[s] = CHAR_EMPTY
                    grid[nextS] = CHAR_SAND
                    hasMoved = True
                    nextSand.append(nextS)
                else:
                    print(f"Sand at {s} couldn't move")
            sand = nextSand
        print("Done simulating cycle!")
        if not hasMoved:
            calculated = countSand(grid)
            print(f"Counted {calculated} units of sand")
            if solution:
                print(f"=> Expecting {solution}")
                assert calculated == solution
            return


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day14-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part1=True, solution=24)

with open("day14-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part1=True, solution=795)

# Part 2
with open("day14-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part1=False, solution=93)

with open("day14-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, part1=False, solution=30214)
