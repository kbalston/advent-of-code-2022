#!/usr/bin/env python3
import os
from collections import deque


def solve(lines: list[str], size: int, solutions: list[int]) -> None:
    for line, solution in zip(lines, solutions):
        print("***")
        print(line)

        answer = 0
        window: deque[str] = deque(maxlen=size)
        for i, c in enumerate(line):
            window.append(c)
            if len(set(window)) == size:
                print(f"{list(window)} is all unique")
                answer = i + 1
                break

        print(f"Solution is {answer}")
        print(f"Expecting   {solution}")
        assert answer == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day6-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=4, solutions=[7, 5, 6, 10, 11])

with open("day6-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=4, solutions=[1909])

# Part 2
with open("day6-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=14, solutions=[19, 23, 23, 29, 26])

with open("day6-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=14, solutions=[3380])
