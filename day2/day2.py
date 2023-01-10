#!/usr/bin/env python3
from __future__ import annotations
import os
from enum import IntEnum


# @@@SNIPSTART day2-MoveType
class MoveType(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
    # @@@SNIPEND

    # @@@SNIPSTART day2-MoveTypeDecode
    @classmethod
    def from_str(cls, rawMove) -> MoveType:
        # We convert these input characters to their ordinal
        # values and then calculate their 'distance' from the base
        # For example, 'B' has a distance of 1 from 'A'
        # and 'C' has a distance of 2 from 'B'
        if rawMove in "ABC":
            dist = ord(rawMove) - ord("A") + 1
        elif rawMove in "XYZ":
            dist = ord(rawMove) - ord("X") + 1
        else:
            assert False, f"Received an unexpected move: {rawMove}"
        # This will throw a `ValueError`
        # if `dist` doesn't map to one of the enum values
        return MoveType(dist)
        # @@@SNIPEND

    def __str__(self) -> str:
        return f"MoveType({self.value}, {self.name[0:5]:>5})"

    # @@@SNIPSTART day2-scoring
    def scoreAgainst(self, oMove: MoveType) -> int:
        # Check for win condition
        if (
            # Formatting disabled to align `if` statement
            # fmt: off
               self == MoveType.ROCK     and oMove == MoveType.SCISSORS
            or self == MoveType.PAPER    and oMove == MoveType.ROCK
            or self == MoveType.SCISSORS and oMove == MoveType.PAPER
            # fmt: on
        ):
            print(f"{self} vs {oMove} -> Win")
            return 6 + int(self)
        # Check for tie condition
        elif int(self) == int(oMove):
            print(f"{self} vs {oMove} -> Tie")
            return 3 + int(self)
        # Else must be lose condition
        else:
            print(f"{self} vs {oMove} -> Lose")
            return 0 + int(self)
            # @@@SNIPEND

    # @@@SNIPSTART day2-deriveMove
    def deriveMove(self, desiredOutcome: str) -> MoveType:
        if desiredOutcome == "Y":
            # Tie
            return self
        elif desiredOutcome == "Z":
            # Win
            if self == MoveType.ROCK:
                return MoveType.PAPER
            if self == MoveType.PAPER:
                return MoveType.SCISSORS
            if self == MoveType.SCISSORS:
                return MoveType.ROCK
        elif desiredOutcome == "X":
            # Lose
            if self == MoveType.ROCK:
                return MoveType.SCISSORS
            if self == MoveType.PAPER:
                return MoveType.ROCK
            if self == MoveType.SCISSORS:
                return MoveType.PAPER
        assert False, (
            f"Unknown error for opponent move of {self} and desired"
            f" outcome of {desiredOutcome}"
        )
        # @@@SNIPEND


# @@@SNIPSTART day2-solvePart1
def solvePart1(lines, solution: int) -> None:
    score = 0
    for line in lines:
        # Get the moves from the puzzle input
        theirMove, ourMove = [
            MoveType.from_str(move) for move in line.split()
        ]
        # Calculate the score
        score += ourMove.scoreAgainst(theirMove)
    print(f"Calculated:  {score:}")
    if solution:
        print(f"=> Expected: {solution}")
    assert solution is None or score == solution
    # @@@SNIPEND


# @@@SNIPSTART day2-solvePart2
def solvePart2(lines, solution: int) -> None:
    score = 0
    for line in lines:
        theirMoveStr, desiredOutcome = line.split()
        theirMove = MoveType.from_str(theirMoveStr)
        ourMove = theirMove.deriveMove(desiredOutcome)
        score += ourMove.scoreAgainst(theirMove)
    print(f"Calculated:  {score}")
    if solution:
        print(f"=> Expected: {solution}")
    assert solution is None or score == solution
    # @@@SNIPEND


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day2-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart1(lines, solution=15)


with open("day2-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart1(lines, solution=14297)

# Part 2
with open("day2-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, solution=12)


with open("day2-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solvePart2(lines, solution=10498)
