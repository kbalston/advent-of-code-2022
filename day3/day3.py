#!/usr/bin/env python3
import os

from itertools import zip_longest
from typing import Optional


# @@@SNIPSTART day3-grouper
# From https://docs.python.org/3/library/itertools.html
# License: Zero Clause BSD License
def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")
        # @@@SNIPEND


# @@@SNIPSTART day3-getScore
def getScore(
    ruckA: str, ruckB: str, ruckC: Optional[str] = None
) -> int:
    """Return the score as an integer of a given elf's rucksack
    or rucksack compartment by finding the first letter
    that is present in all provided rucksacks.

    Will assert if no letters are found in common.
    """
    for letter in ruckA:
        if letter in ruckB and (ruckC is None or letter in ruckC):
            print(f"=> found '{letter}' in all")
            if letter.islower():
                return ord(letter) - ord("a") + 1
            else:
                return ord(letter) - ord("A") + 27
    assert False, "Unable to find a common letter"
    # @@@SNIPEND


def checkSolution(calculated: int, expected: int) -> None:
    print("*" * 10)
    print(f"Score is     {calculated}")
    if expected is not None:
        print(f"=> Expecting {expected}")
        assert calculated == expected


# @@@SNIPSTART day3-part1
def solvePart1(lines: list[str], expected: int) -> None:
    calculated = 0
    spacer = "=" * 10
    for i, line in enumerate(lines, start=1):
        print(f"{spacer} Part 1: Rucksack {i} {spacer}")
        halfway = int(len(line) / 2)
        # Divide into two compartments
        firstCompartment = line[0:halfway]
        secondCompartment = line[halfway:]
        print(firstCompartment)
        print(secondCompartment)
        # Find the first shared letter in the compartments
        calculated += getScore(firstCompartment, secondCompartment)
    checkSolution(calculated=calculated, expected=expected)
    # @@@SNIPEND


# @@@SNIPSTART day3-part2
def solvePart2(lines: list[str], expected: int) -> None:
    calculated = 0
    spacer = "=" * 10
    # Group in strict mode so if an iteration has fewer than
    # `n` items, `grouper` asserts
    iterator = grouper(iterable=lines, n=3, incomplete="strict")
    for i, elves in enumerate(iterator, start=1):
        print(f"{spacer} Part 2: Rucksack {i} {spacer}")
        for elf in elves:
            print(elf)
        # Find the first shared letter in the compartments
        calculated += getScore(*elves)
    checkSolution(calculated=calculated, expected=expected)
    # @@@SNIPEND


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day3-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart1(lines, expected=157)

with open("day3-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart1(lines, expected=7746)

with open("day3-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, expected=70)

with open("day3-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, expected=2604)
