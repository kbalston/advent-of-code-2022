#!/usr/bin/env python3

import os
import re
from collections import deque
from typing import Any, Optional


# @@@SNIPSTART day5-parseCratePositions
def parseCratePositions(
    lines: list[str],
) -> list[deque[Any]]:
    spots: Optional[list[deque[Any]]] = None
    while lines:
        line = lines.pop(0)
        print(f"\nParsing line '{line}'")
        # There's likely a more elegant way of detecting
        # the transition from crate state to movement list
        # however for now it's likely fine to just look for the
        # column numbers like " 1   2   3"
        if "1" in line:
            print(
                f"=> Detected a '1' in the line"
                f" => Assuming end of crate list"
            )
            # Also pop the next line, which should be empty
            nextLine = lines.pop(0)
            assert nextLine == ""
            assert spots is not None
            return spots

        index = 0
        values = []
        # For this line we're parsing right now,
        # read three characters at a time and decode as a crate
        while True:
            crate = line[index : index + 3]
            assert crate is not None
            # Check for no crate in this spot
            if crate == "   ":
                value = None
            else:
                # Take the middle position as the crate
                value = crate[1]
            values.append(value)
            index += 4
            if index > len(line):
                # Done reading all crates at this height
                break
        print(f"=> Received {values}")
        assert values
        # Lazily allocate this since we don't know up front
        # how many columns we need
        if spots is None:
            spots = [deque() for _ in values]
            spots.append(deque())
        # Append this line's crate positions into `spots`
        for i, letter in enumerate(values):
            if letter is not None:
                print(f"==> {letter} is at index {i + 1}")
                spots[i + 1].append(letter)
    assert False
    # @@@SNIPEND


# @@@SNIPSTART day5-executeCrateMoves
def executeCrateMoves(
    spots: list[deque[str]], lines: list[str], moveMultiple: bool
) -> None:
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in lines:
        # Parse the line into relevant variables
        print(f"\nParsing line '{line}'")
        matches = re.match(pattern, line)
        assert matches
        moves = int(matches.group(1))
        source = int(matches.group(2))
        dest = int(matches.group(3))
        assert spots is not None
        # Perform the movement
        # Part 1 - move each crate directly to the destination, one by one
        if not moveMultiple:
            for move in range(moves):
                print(f"=> Moving #{move} from {source} to {dest}")
                crate = spots[source].popleft()
                spots[dest].appendleft(crate)
        # Part 2 - move each crate to `cratesToMove` temporarily
        # before moving them to their final destination
        # Compared to part 1, when groups of crates are moved together,
        # they will not have their positions reversed
        else:
            cratesToMove: deque[str] = deque()
            for move in range(moves):
                print(f"=> Moving #{move} from {source} to {dest}")
                crate = spots[source].popleft()
                cratesToMove.appendleft(crate)
            for crate in cratesToMove:
                spots[dest].appendleft(crate)
    # @@@SNIPEND


# @@@SNIPSTART day5-extractSolution
def extractSolution(spots: list[deque[str]]) -> str:
    # Returns the topmost crate if it exists,
    # otherwise it returns an empty string
    def extractFirst(crates: deque[str]) -> str:
        if len(crates) > 0:
            return crates[0]
        else:
            return ""

    # Concatenate together the topmost crate from each position
    return "".join(map(extractFirst, spots))
    # @@@SNIPEND


# @@@SNIPSTART day5-solve
def solve(
    lines: list[str], moveMultiple: bool, solution: str
) -> None:
    # Step 1: Parse initial state
    print("*** Parsing initial crate state ***")
    spots = parseCratePositions(lines)

    # Step 2: Execute crate movement from list
    print("\n*** Executing crate moves ***")
    executeCrateMoves(spots, lines, moveMultiple)

    # Step 3: Extract solution topmost crates in each column
    calculated = extractSolution(spots)

    print()
    print(f"Solution is {calculated}")
    print(f"Expecting   {solution}")
    assert calculated == solution
    # @@@SNIPEND


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day5-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, moveMultiple=False, solution="CMZ")

with open("day5-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, moveMultiple=False, solution="SPFMVDTZT")

with open("day5-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, moveMultiple=True, solution="MCD")

with open("day5-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, moveMultiple=True, solution="ZFSJBPRFP")
