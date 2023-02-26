#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
import logging
import os
from collections import defaultdict
from typing import Optional, Sequence

logging.basicConfig(format="%(message)s", level=logging.INFO)


@dataclass(frozen=True)
class Plan:
    source: Pos
    destination: Pos


@dataclass(frozen=True)
class Pos:
    y: int
    x: int

    def north(self) -> Sequence[Pos]:
        return (
            Pos(self.y - 1, self.x - 1),
            Pos(self.y - 1, self.x + 0),
            Pos(self.y - 1, self.x + 1),
        )

    def south(self) -> Sequence[Pos]:
        return (
            Pos(self.y + 1, self.x - 1),
            Pos(self.y + 1, self.x + 0),
            Pos(self.y + 1, self.x + 1),
        )

    def east(self) -> Sequence[Pos]:
        return (
            Pos(self.y - 1, self.x + 1),
            Pos(self.y + 0, self.x + 1),
            Pos(self.y + 1, self.x + 1),
        )

    def west(self) -> Sequence[Pos]:
        return (
            Pos(self.y - 1, self.x - 1),
            Pos(self.y + 0, self.x - 1),
            Pos(self.y + 1, self.x - 1),
        )

    def all(self) -> Sequence[Pos]:
        ret = list(self.north())
        ret.extend(self.south())
        # For east and west, only need pure-east and pure-west
        ret.extend(self.east()[1:2])
        ret.extend(self.west()[1:2])
        return ret


def score(table: defaultdict[Pos, str]) -> int:
    minX = None
    maxX = None
    minY = None
    maxY = None
    for pos, v in list(table.items()):
        if v == "#":
            if minX is None or minX > pos.x:
                minX = pos.x
            if minY is None or minY > pos.y:
                minY = pos.y

            if maxX is None or maxX < pos.x:
                maxX = pos.x
            if maxY is None or maxY < pos.y:
                maxY = pos.y

    s = 0
    assert minX is not None
    assert maxX is not None
    assert minY is not None
    assert maxY is not None
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            v = table[Pos(y=y, x=x)]
            if v == ".":
                s += 1

    return s


def printMap(table: defaultdict[Pos, str]) -> None:
    minX = None
    maxX = None
    minY = None
    maxY = None
    for pos, v in list(table.items()):
        if v == "#":
            if minX is None or minX > pos.x:
                minX = pos.x
            if minY is None or minY > pos.y:
                minY = pos.y

            if maxX is None or maxX < pos.x:
                maxX = pos.x
            if maxY is None or maxY < pos.y:
                maxY = pos.y

    margin = 2
    assert minX is not None
    assert maxX is not None
    assert minY is not None
    assert maxY is not None
    for y in range(minY - margin, maxY + 1 + margin):
        for x in range(minX - margin, maxX + 1 + margin):
            print(table[Pos(y=y, x=x)], end="")
        print()
    print()


def solve(
    lines: list[str],
    rounds: Optional[int],
    solutionEmptyGroundTiles: Optional[int],
    solutionRoundCompletion: Optional[int],
) -> None:
    table: defaultdict[Pos, str] = defaultdict(lambda: ".")
    for y, line in enumerate(lines, start=0):
        for x, v in enumerate(line, start=0):
            pos = Pos(y=y, x=x)
            # TODO: Consider having true/false indicate elf presence
            # and not storing empty spots
            table[pos] = v

    shouldPrintMap = False

    if rounds is None:
        rounds = 100000

    for round in range(1, rounds + 1):
        logging.info(f"Simulating round {round}...")
        plans: dict[Pos, Optional[Plan]] = dict()
        for pos, v in list(table.items()):
            if v == "#":
                logging.debug(f"\n[{pos}] Calculating move")
                # Check around
                allPos = pos.all()
                for cc in allPos:
                    if table[cc] == "#":
                        logging.debug(
                            f"  [{pos}] There is an elf around"
                        )
                        around = True
                        break
                else:
                    logging.debug(
                        f"  [{pos}] There isn't an elf around"
                    )
                    around = False
                # Propose
                if around:
                    # four cardinal directions
                    for i in range(4):
                        match ((round - 1) + i) % 4:
                            case 0:
                                direction = pos.north
                            case 1:
                                direction = pos.south
                            case 2:
                                direction = pos.west
                            case 3:
                                direction = pos.east
                            case _:
                                assert False
                        logging.debug(
                            f"  [{pos}] Checking {direction.__name__}"
                        )
                        c = direction()
                        for cc in c:
                            if table[cc] == "#":
                                logging.debug(
                                    f"    [{pos}] There is an elf"
                                    " in the"
                                    f" {direction.__name__} direction"
                                    " so NOT going to propose a"
                                    " move"
                                )
                                move = False
                                break
                        else:
                            logging.debug(
                                f"    [{pos}] There isn't an elf"
                                " in the"
                                f" {direction.__name__} direction"
                                " so going to propose a move via"
                                f" {direction.__name__}"
                            )
                            move = True

                        if move:
                            # When moving, we only move in one of the four cardinal directions
                            # which corresponds with the middle value in the tuple we receive
                            _, dest, _ = direction()
                            logging.debug(
                                f"  [{pos}] Proposing move to {dest}"
                            )
                            if dest in plans:
                                plans[dest] = None
                            else:
                                thisPlan = Plan(
                                    source=pos, destination=dest
                                )
                                plans[dest] = thisPlan
                            break
        # Do moves
        for p in plans.values():
            if p is None:
                continue
            logging.debug(
                f"Moving elf from {p.source} to {p.destination}"
            )
            assert table[p.source] == "#"
            table[p.source] = "."
            assert table[p.destination] == "."
            table[p.destination] = "#"
        logging.info(f"=> {len(plans)} elves moved this round")
        if len(plans) == 0:
            logging.info(
                f"=> All elves stopped moving at round {round}"
            )
            break
        plans.clear()
        logging.info(f"Round {round} complete")
        if shouldPrintMap:
            printMap(table)

    logging.info(f"Completed after round {round}")
    if solutionRoundCompletion is not None:
        logging.info(
            f"=> Expected solution: {solutionRoundCompletion}"
        )
        assert round == solutionRoundCompletion

    emptyGroundTiles = score(table)
    logging.info(
        f"Calculated empty ground tiles:  {emptyGroundTiles}"
    )
    if solutionEmptyGroundTiles is not None:
        logging.info(
            f"=> Expected solution: {solutionEmptyGroundTiles}"
        )
        assert emptyGroundTiles == solutionEmptyGroundTiles


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day23-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=10,
    solutionEmptyGroundTiles=110,
    solutionRoundCompletion=None,
)

with open("day23-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=10,
    solutionEmptyGroundTiles=4075,
    solutionRoundCompletion=None,
)

# Part 2
with open("day23-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=None,
    solutionEmptyGroundTiles=None,
    solutionRoundCompletion=20,
)

with open("day23-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=None,
    solutionEmptyGroundTiles=None,
    solutionRoundCompletion=950,
)
