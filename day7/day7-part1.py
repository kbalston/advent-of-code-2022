#!/usr/bin/env python3
import os
import re
from collections import deque


def solve(lines, size, solutions=[None]):
    for line, solution in zip(lines, solutions):
        answer = 0
        print(line)
        print(solution)

        window = deque(maxlen=size)
        for i, c in enumerate(line):
            window.append(c)
            if len(set(window)) == size:
                print(f"{window} is all unique")
                answer = i + 1
                break

        assert solution is None or answer == solution
    return answer


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day7-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=4, solutions=[7, 5, 6, 10, 11])

with open("day7-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, size=4, solutions=[None])
