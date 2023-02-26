#!/usr/bin/env python3

from __future__ import annotations
import itertools

import os
from typing import cast
import logging


logging.basicConfig(format="%(message)s", level=logging.INFO)


class Cube(tuple[int, int, int]):
    pass


def solvePart1(cubes: dict[tuple[int, int, int], bool]) -> int:
    sa = 0
    cubesToCheck = cubes
    for cube in cubesToCheck:
        logging.debug(f"==> Looking for cubes adjacent to {cube}")
        for dim in range(3):
            for modifier in (-1, 1):
                c = list(cube)
                c[dim] += modifier
                logging.debug(f"===> Checking {c}")
                # mypy is unable to automatically infer the size of these tuples
                c2 = cast(tuple[int, int, int], tuple(c))
                if cubes.get(c2, None):
                    pass
                else:
                    sa += 1
                pass
    return sa


def solvePart2(
    cubes: dict[tuple[int, int, int], bool],
    maxIterations: int = 10000,
) -> int:
    allMax = 0
    allMin = 100
    for c in cubes:
        thisMax = max(*c)
        allMax = max(allMax, thisMax)
        thisMin = min(*c)
        allMin = min(allMin, thisMin)
    boundMin = allMin - 1
    boundMax = allMax + 1
    sa = 0
    # Lets try a floodfill
    cubesToCheckNext = list()
    start = (0, 0, 0)
    cubesToCheckNext.append(start)
    cubesQueued = list()
    cubesQueued.append(start)
    for iteration in range(maxIterations):
        logging.debug(f"Iteration {iteration} (sa={sa})")
        cubesToCheck = cubesToCheckNext
        cubesToCheckNext = list()
        if len(cubesToCheck) == 0:
            logging.debug("No cubes to check => ending early")
            break
        for cube in cubesToCheck:
            logging.debug(f"=> From {cube}")
            for dim, modifier in itertools.product(range(3), (-1, 1)):
                # FIXME: More elegant way of creating this?
                # toCheck = cube[:dim] + (cube[dim:dim] + modifier) + cube[dim+1:]
                toCheck: list[int] = list(cube)
                toCheck[dim] += modifier
                if toCheck[dim] < boundMin or toCheck[dim] > boundMax:
                    logging.debug(f"==> Not checking {toCheck} (OOB)")
                    continue
                elif tuple(toCheck) in cubes:
                    logging.debug(
                        f"==> Not checking {toCheck} (solid)"
                    )
                    sa += 1
                    continue
                elif tuple(toCheck) in cubesQueued:
                    logging.debug(
                        f"==> Not checking {toCheck} (seen)"
                    )
                    continue
                else:
                    logging.debug(
                        f"==>     Checking {toCheck} next iteration"
                    )
                    # mypy is unable to automatically infer the size of these tuples
                    toCheck2 = cast(
                        tuple[int, int, int], tuple(toCheck)
                    )
                    cubesQueued.append(toCheck2)
                    cubesToCheckNext.append(toCheck2)
    return sa


def solve(lines: list[str], part1: bool, solution: int) -> None:
    # Read in data
    cubes: dict[tuple[int, int, int], bool] = dict()
    for i, line in enumerate(lines, start=1):
        pos = (int(x) for x in line.split(","))
        cube = Cube(pos)
        cubes[cube] = True

    if part1:
        calculated = solvePart1(cubes)
    else:
        calculated = solvePart2(cubes)

    logging.info(f"Calculated:  {calculated}")
    logging.info(f"=> Expecting {solution}")
    assert calculated == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day18-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    solution=64,
)

with open("day18-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    solution=3564,
)

# Part 2
with open("day18-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    solution=58,
)

with open("day18-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    solution=2106,
)
