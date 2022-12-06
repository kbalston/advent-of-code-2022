#!/usr/bin/env python3
import os
import re
from collections import deque

# Check if a is contained within b
def isContainedWithin(a, b):
    # If b[0] is lower than or equal to a[0]
    # and b[1] is greater than or equal to a[1]
    # Then a is fully in b
    if b[0] <= a[0] and b[1] >= a[1]:
        print(f"*** {a} is fully in {b}")
        return True
    else:
        print(f"{a} is NOT fully in {b}")
        return False


class Elf:
    pass


def solve(lines, solution=None):
    score = 0

    spots = None
    while lines:
        line = lines.pop(0)
        print(f"Line='{line}'")
        if "1" in line:
            emptyLine = lines.pop(0)
            assert emptyLine == ""
            break

        index = 0
        values = []
        while True:
            value = line[index : index + 3]
            index += 4
            if value == "   ":
                value = None
            else:
                value = value[1]
            values.append(value)
            if index > len(line):
                break
        print(f"=> got {values}")

        # pattern = "((?:   )|(?:\[\w\]))"
        # values = re.findall(pattern, line)
        assert values
        if spots is None:
            spots = [deque() for i in values]
            spots.append(deque())
        print(values)
        for i, letter in enumerate(values):
            if not letter is None:
                print(f"=> {letter} is at index {i + 1}")
                spots[i + 1].append(letter)

    print("Starting moves")

    while lines:
        line = lines.pop(0)
        print(f"Line='{line}'")
        pattern = "move (\d+) from (\d+) to (\d+)"
        matches = re.match(pattern, line)
        # print(matches.groups())
        moves = int(matches.group(1))
        source = int(matches.group(2))
        dest = int(matches.group(3))
        for move in range(moves):
            print(f"=> Moving [{move}] from {source} to {dest}")
            # if len(spots[source]):
            letter = spots[source].popleft()
            spots[dest].appendleft(letter)

    score = ""
    assert len(spots[0]) == 0
    for spot in spots:
        if spot:
            score += spot.popleft()
    print(f"Solution is {score}")
    assert score == solution or solution is None


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day5-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution="MCD")

with open("day5-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines)
# Not NRGFVCTGH
