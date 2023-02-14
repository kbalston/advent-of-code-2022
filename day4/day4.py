#!/usr/bin/env python3
import os
from typing import List


# @@@SNIPSTART day4-elfpair
class ElfPair:
    def __init__(self) -> None:
        # A simple two-dimensional list of integers
        # Intent is that:
        # The first index corresponds with the elf
        #   e.g., self.assignments[1] corresponds with Elf B
        # The second index corresponds with
        #   the lower and upper bounds of that elf's assignment
        #   e.g., self.assignments[1][0] corresponds with
        #   Elf B's lower assignment bound
        self.assignments: List[List[int]] = []

    def __str__(self) -> str:
        return f"Elf={self.assignments}"

    def addAssignment(self, assignments: list[int]) -> None:
        self.assignments.append(assignments)

    def getAssignmentSet(self, index: int) -> set[int]:
        assert len(self.assignments) >= index
        return set(
            range(
                self.assignments[index][0],
                self.assignments[index][1] + 1,
            )
        )
        # @@@SNIPEND

    # @@@SNIPSTART day4-hasoverlap
    # Within ElfPair class
    def hasOverlap(self, requireFullOverlap: bool) -> bool:
        assert len(self.assignments) == 2
        elfA = self.getAssignmentSet(0)
        elfB = self.getAssignmentSet(1)

        # Part 1
        if requireFullOverlap:
            # Full overlap requires one of these
            # ranges to be a subset of the other
            return elfA.issubset(elfB) or elfB.issubset(elfA)
        # Part 2
        else:
            # Partial overlap just requires these sets to not be disjoint
            # e.g., there is at least one shared number between these two sets
            return not elfA.isdisjoint(elfB)
        # @@@SNIPEND


# @@@SNIPSTART day4-solve
def solve(
    lines: list[str], solution: int, requireFullOverlap: bool
) -> None:
    pairs = []

    # Read in data line-by-line
    for line in lines:
        # Split string on , to extract the ranges
        split = line.split(",")
        # Then split on - to get the bounds
        first = split[0].split("-")
        second = split[1].split("-")
        pair = ElfPair()
        # Ingest the upper and lower bounds into the `ElfPair`
        pair.addAssignment([int(x) for x in first])
        pair.addAssignment([int(x) for x in second])
        pairs.append(pair)

    # Iterate through elf pairs and find overlap
    score = 0
    for i, pair in enumerate(pairs, start=1):
        print(f"Checking elf pair {i:>4}: {pair}", end="")
        if pair.hasOverlap(requireFullOverlap):
            score += 1
            print(" -> has overlap")
        else:
            print(" -> does NOT have overlap")

    print(f"Solution is  {score}")
    print(f"=> Expecting {solution}\n")
    assert score == solution
    # @@@SNIPEND


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day4-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=2, requireFullOverlap=True)

with open("day4-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=513, requireFullOverlap=True)

with open("day4-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=4, requireFullOverlap=False)

with open("day4-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=878, requireFullOverlap=False)
