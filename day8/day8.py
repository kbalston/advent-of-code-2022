#!/usr/bin/env python3

from collections import defaultdict
import functools
import operator
import os


class Spot:
    def __init__(self, y: int, x: int, char: str) -> None:
        self.y = y
        self.x = x
        self.height = int(char)
        self.visible = False
        self.viewingDistances: list[int] = []

    def __repr__(self) -> str:
        return f"Spot{{{self.height}@{self.y},{self.x}}}"

    def score(self) -> int:
        return functools.reduce(
            operator.mul, self.viewingDistances, 1
        )


def solve(
    lines: list[str], solutionPart1: int, solutionPart2: int
) -> None:
    # Parse into data structure
    table: defaultdict[int, dict[int, Spot]] = defaultdict(dict)
    maxY = 0
    maxX = 0
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            print(f"[{y}][{x}]: {char}")
            table[y][x] = Spot(y, x, char)
    maxY = len(table)
    maxX = len(table[y])
    print("----")
    visibleCount = 0
    print(f"maxY: {maxY}")
    print(f"maxX: {maxX}")
    bestScore = 0
    for y in range(maxY):
        for x in range(maxX):
            print(f"\n[{y}][{x}]: {table[y][x]}")
            print("=> Considering if visible")

            if y == 0 or y == maxY - 1 or x == 0 or x == maxX - 1:
                print("==> Is on the periphery => Visible")
                table[y][x].visible = True
            else:
                xi = x
                print("==> Checking up (subtract y)")
                for i, yi in enumerate(range(y - 1, -1, -1)):
                    print(
                        f"===> Checking [{yi}][{xi}] =>"
                        f" {table[yi][xi].height}"
                    )
                    if table[yi][xi].height >= table[y][x].height:
                        table[y][x].viewingDistances.append(i + 1)
                        break
                else:
                    print("==> Visible")
                    table[y][x].viewingDistances.append(i + 1)
                    table[y][x].visible = True
                print(f"==> Viewing distance is {i + 1}")

                print("==> Checking down (add y)")
                xi = x
                for i, yi in enumerate(range(y + 1, maxY, +1)):
                    print(
                        f"===> Checking [{yi}][{xi}] =>"
                        f" {table[yi][xi].height}"
                    )
                    if table[yi][xi].height >= table[y][x].height:
                        table[y][x].viewingDistances.append(i + 1)
                        break
                else:
                    print("==> Visible")
                    table[y][x].viewingDistances.append(i + 1)
                    table[y][x].visible = True
                print(f"==> Viewing distance is {i + 1}")

                print("==> Checking left (subtract x)")
                yi = y
                for i, xi in enumerate(range(x - 1, -1, -1)):
                    print(
                        f"===> Checking [{yi}][{xi}] =>"
                        f" {table[yi][xi].height}"
                    )
                    if table[yi][xi].height >= table[y][x].height:
                        table[y][x].viewingDistances.append(i + 1)
                        break
                else:
                    print("==> Visible")
                    table[y][x].viewingDistances.append(i + 1)
                    table[y][x].visible = True
                print(f"==> Viewing distance is {i + 1}")

                print("==> Checking right (add x)")
                yi = y
                for i, xi in enumerate(range(x + 1, maxX, +1)):
                    print(
                        f"===> Checking [{yi}][{xi}] =>"
                        f" {table[yi][xi].height}"
                    )
                    if table[yi][xi].height >= table[y][x].height:
                        table[y][x].viewingDistances.append(i + 1)
                        break
                else:
                    print("==> Visible")
                    table[y][x].viewingDistances.append(i + 1)
                    table[y][x].visible = True
                print(f"==> Viewing distance is {i + 1}")

            # Done checking heights in cardinal directions
            if table[y][x].visible:
                visibleCount += 1
            print(
                "==> Viewing distances are"
                f" {table[y][x].viewingDistances}"
            )
            print(f"==> Viewing score is {table[y][x].score()}")
            bestScore = max(bestScore, table[y][x].score())
    # Part 1
    print(f"\nTotal of {visibleCount} trees visible")
    if solutionPart1:
        print(f"=> Expecting {solutionPart1} trees")
        assert visibleCount == solutionPart1
    # Part 2
    print(f"\nBest viewing score is {bestScore}")
    if solutionPart2:
        print(f"=> Expecting best viewing score of {solutionPart2}")
        assert bestScore == solutionPart2


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day8-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solutionPart1=21, solutionPart2=8)

with open("day8-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solutionPart1=1736, solutionPart2=268800)
