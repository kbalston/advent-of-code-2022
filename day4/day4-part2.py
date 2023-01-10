#!/usr/bin/env python3
import os


# Check if a is contained within b
def overlapAtAll(a, b):
    # If b[0] is lower than or equal to a[0]
    # and b[1] is greater than or equal to a[1]
    # Then a is fully in b
    bb = range(b[0], b[1] + 1)
    aa = range(a[0], a[1] + 1)
    bbs = set(bb)
    overlaps = bbs.intersection(aa)
    return len(overlaps) > 0
    # if b[0] <= a[0] or b[1] >= a[1]:
    #     print(f"*** {a} is fully in {b}")
    #     return True
    # else:
    #     print(f"{a} is NOT fully in {b}")
    #     return False


class Elf:
    pass


def solve(lines, solution=None):
    score = 0
    elves = []
    for line in lines:
        split = line.split(",")
        first = split[0].split("-")
        second = split[1].split("-")
        elf = Elf()
        elf.assignments = []
        elf.assignments.append([int(x) for x in first])
        elf.assignments.append([int(x) for x in second])
        # assignments.append(first)
        # assignments.append(second)
        elves.append(elf)
        # print(line)
    for elf in elves:
        print(f"-- Checking elf {elf}")
        if overlapAtAll(elf.assignments[0], elf.assignments[1]):
            score += 1
            continue
        if overlapAtAll(elf.assignments[1], elf.assignments[0]):
            score += 1
            continue
    # while elves:
    #     elfA = elves.pop(0)
    #     for elfB in elves:
    #         for i in (0,1):
    #             fullyContained = isContainedWithin(elfA.assignments[i], elfB.assignments[i])
    #             if fullyContained:
    #                 elves.remove(elfB)
    #                 score += 1
    #                 break

    print(f"Solution is {score}")
    assert score == solution or solution is None


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day4-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=4)

with open("day4-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines)
# Not 566
# Not 537
