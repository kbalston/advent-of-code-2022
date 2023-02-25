#!/usr/bin/env python3

from __future__ import annotations
from functools import cmp_to_key
from itertools import zip_longest

import os
from typing import Optional, Union
import ast


def compare(
    left: Union[int, list[int]],
    right: Union[int, list[int]],
    depth: int,
    quiet: bool = True,
) -> Optional[bool]:
    indent = "  " * depth
    indentPlusOne = "  " * (depth + 1)
    if not quiet:
        print(f"{indent}- Compare {left} vs {right}")
    # If both values are integers...
    if isinstance(left, int) and isinstance(right, int):
        left = int(left)
        right = int(right)
        if left == right:
            return None
        elif left < right:
            if not quiet:
                print(
                    f"{indentPlusOne}- Left side is smaller, so"
                    " inputs are in the right order"
                )
            return True
        elif left > right:
            if not quiet:
                print(
                    f"{indentPlusOne}- Right side is smaller, so"
                    " inputs are not in the right order"
                )
            return False
        else:
            assert False
    # If both values are lists
    elif isinstance(left, list) and isinstance(right, list):
        for leftI, rightI in zip_longest(left, right):
            if leftI is None:
                if not quiet:
                    print(
                        f"{indentPlusOne}- Left side ran out of"
                        " items, so inputs are in the right order"
                    )
                return True
            elif rightI is None:
                if not quiet:
                    print(
                        f"{indentPlusOne}- Right side ran out of"
                        " items, so inputs are not in the right"
                        " order"
                    )
                return False
            else:
                r = compare(leftI, rightI, depth + 1)
                if r is not None:
                    return r
        return None
    elif isinstance(left, list) and isinstance(right, int):
        if not quiet:
            print(
                f"{indentPlusOne}- Mixed types; convert right to []"
                " and retry comparison"
            )
        r = compare(left, [right], depth)
        if r is not None:
            return r
        return None
    elif isinstance(left, int) and isinstance(right, list):
        if not quiet:
            print(
                f"{indentPlusOne}- Mixed types; convert left to []"
                " and retry comparison"
            )
        r = compare([left], right, depth)
        if r is not None:
            return r
        return None
    else:
        assert False


def compareFunction(
    left: Union[int, list[int]], right: Union[int, list[int]]
) -> int:
    r = compare(left, right, 0)
    if r is True:
        return -1
    elif r is None:
        return 0
    else:
        return 1


def solve(lines: list[str], solution: int) -> None:
    linesI = iter(lines)
    pairCount = 0
    sum = 0
    while linesI:
        print("============")
        pairCount += 1
        left = ast.literal_eval(next(linesI))
        right = ast.literal_eval(next(linesI))
        r = compare(left, right, 0)
        if r is True:
            sum += pairCount
        try:
            empty = next(linesI)
            assert empty == ""
        except StopIteration:
            break

    print(f"Sum is {sum}")
    print(f"=> Expecting {solution}")
    assert sum == solution


def solvePart2(lines: list[str], solution: int) -> None:
    linesNonNull = filter(None, (line.rstrip() for line in lines))
    linesEvaled = [ast.literal_eval(line) for line in linesNonNull]
    decoder1 = [[2]]
    decoder2 = [[6]]
    linesEvaled.append(decoder1)
    linesEvaled.append(decoder2)

    linesOrdered = sorted(
        linesEvaled, key=cmp_to_key(compareFunction)
    )

    sum = None
    for i, line in enumerate(linesOrdered, start=1):
        if line is decoder1 or line is decoder2:
            print(f"Found decoder at index {i}")
            if sum is None:
                sum = i
            else:
                sum = sum * i
                break

    print(f"Sum is {sum}")
    if solution is not None:
        print(f"=> Expecting {solution}")
        assert sum == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day13-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=13)

with open("day13-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=5580)

# Part 2
with open("day13-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, solution=140)

with open("day13-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, solution=26200)
