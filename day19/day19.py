#!/usr/bin/env python3

from __future__ import annotations

import copy
import itertools
import os
import random
import re
from collections import deque
from enum import IntEnum, auto
import time
from typing import Iterable, Optional

from rich import print  # type: ignore


class Resources:
    def __init__(
        self, ore: int, clay: int, obsidian: int, geode: int
    ) -> None:
        self.ore = ore
        self.clay = clay
        self.obsidian = obsidian
        self.geode = geode


class BuyOrder(IntEnum):
    UNINITIALIZED = auto()
    BUY_GEODE = auto()
    BUY_OBSIDIAN = auto()
    BUY_CLAY = auto()
    BUY_ORE = auto()
    BUY_NONE = auto()
    DONE = auto()


class State:
    def __init__(
        self,
        blueprint: Blueprint,
        resources: Resources,
        robots: Resources,
    ) -> None:
        self.blueprint = blueprint
        self.resources = resources
        self.robots = robots
        self.buyOrder = BuyOrder.UNINITIALIZED

    def canBuy(self, buyOrder: BuyOrder) -> bool:
        match buyOrder:
            case BuyOrder.BUY_GEODE:
                return (
                    self.resources.ore
                    >= self.blueprint.geodeRobotCost[0]
                    and self.resources.obsidian
                    >= self.blueprint.geodeRobotCost[1]
                )
            case BuyOrder.BUY_OBSIDIAN:
                return (
                    self.resources.ore
                    >= self.blueprint.obsidianRobotCost[0]
                    and self.resources.clay
                    >= self.blueprint.obsidianRobotCost[1]
                )
            case BuyOrder.BUY_CLAY:
                return (
                    self.resources.ore >= self.blueprint.clayRobotCost
                )
            case BuyOrder.BUY_ORE:
                return (
                    self.resources.ore >= self.blueprint.oreRobotCost
                )
            case _:
                assert False

    # Update the buyOrder to the next thing to try
    # Returns true if order was successfully iterated, false otherwise
    def nextOrder(self) -> bool:
        # DFS Strategy
        # Optimization 2: If we previously bought a geode, don't even bother
        # exploring other options
        if self.buyOrder == BuyOrder.BUY_GEODE:
            return False
        while True:
            if self.buyOrder == BuyOrder.DONE:
                return False
            self.buyOrder = BuyOrder(self.buyOrder + 1)

            match self.buyOrder:
                case BuyOrder.UNINITIALIZED:
                    assert False
                case BuyOrder.BUY_GEODE:
                    if self.canBuy(BuyOrder.BUY_GEODE):
                        return True
                case BuyOrder.BUY_OBSIDIAN:
                    if self.canBuy(BuyOrder.BUY_OBSIDIAN):
                        return True
                case BuyOrder.BUY_CLAY:
                    if self.canBuy(BuyOrder.BUY_CLAY):
                        # Optimization 3: Don't buy a clay robot
                        # if we're already making so much clay per
                        # turn that we can build anything
                        if (
                            self.robots.clay
                            >= self.blueprint.obsidianRobotCost[1]
                        ):
                            continue
                        return True
                case BuyOrder.BUY_ORE:
                    if self.canBuy(BuyOrder.BUY_ORE):
                        # Optimization 4: Don't buy an ore robot
                        # if we're already making so much ore per
                        # turn that we can build anything
                        if (
                            self.robots.ore
                            >= self.blueprint.maxOreCost
                        ):
                            continue
                        return True
                case BuyOrder.BUY_NONE:
                    return True
                case BuyOrder.DONE:
                    return False
                case _:
                    assert False


def convertToMillion(number: int) -> str:
    numberAsFloat = number / 1000000
    return f"{numberAsFloat:5.1f} M"


class Blueprint:
    def __init__(
        self,
        name: str,
        minutes: int,
        oreRobotCost: str,
        clayRobotCost: str,
        obsidianRobotCost: Iterable[str],
        geodeRobotCost: Iterable[str],
    ) -> None:
        self.name = name
        self.currentMinute = 1
        self.totalMinutes = minutes
        self.state: deque[State] = deque()
        self.initState()
        # Costs ore
        self.oreRobotCost = int(oreRobotCost)
        # Costs ore
        self.clayRobotCost = int(clayRobotCost)
        # Costs ore, clay
        self.obsidianRobotCost = tuple(
            int(x) for x in obsidianRobotCost
        )
        # Costs ore, obsidian
        self.geodeRobotCost = tuple(int(x) for x in geodeRobotCost)
        self.maxOreCost = max(
            (
                self.oreRobotCost,
                self.clayRobotCost,
                self.obsidianRobotCost[0],
                self.geodeRobotCost[0],
            )
        )

    def initState(self) -> None:
        startResources = Resources(0, 0, 0, 0)
        startRobots = Resources(1, 0, 0, 0)
        self.state.clear()
        self.state.append(
            State(
                blueprint=self,
                resources=startResources,
                robots=startRobots,
            )
        )

    def sim(self) -> tuple[int, int, int]:
        verbose = False
        startTime = time.time()
        best = 0
        statesSeen = 0
        mostGeode = [0] * self.totalMinutes
        mostGeodePrunes = 0
        # These strategies were a technique for seeding the search space with
        # a given buy strategy to start, before backtracking, with the intent
        # to allow us to do early elimination of a number of low-value paths
        # In the end, this wasn't necessary, but more generally the technique
        # may still be a good idea
        strategies: list[tuple[int, ...]] = list(
            itertools.product([1, 2, 3], repeat=3)
        )
        # strategies: list[tuple[int, ...]] = list()
        i = 0
        while True:
            if verbose:
                print("**** New simulation ****")
            if strategies and i < len(strategies):
                strategy = strategies[i]
            else:
                strategy = None
            # strategy = None
            i += 1
            # Fill up the state
            while len(self.state) <= self.totalMinutes:
                minute = len(self.state) - 1
                if verbose:
                    print(f"== Minute {minute + 1} ==")

                # Optimization 1
                # Prune any path that has fewer geode robots than previously seen
                # It is likely it will never catch up
                thisGeodeRobots = self.state[minute].robots.geode
                if thisGeodeRobots > mostGeode[minute]:
                    mostGeode[minute] = thisGeodeRobots
                elif mostGeode[minute] - thisGeodeRobots >= 2:
                    # prune
                    mostGeodePrunes += 1
                    # break to prune all adjacent paths as well
                    break

                # Set buyOrder
                self.executeBuyOrderStrategy(strategy, minute)

                # Create next state based on current state
                self.state.append(copy.deepcopy(self.state[minute]))
                self.state[minute + 1].buyOrder = (
                    BuyOrder.UNINITIALIZED
                )

                # Any prunes below this point will only prune this particular branch
                # rather than all adjacent paths as well

                # Optimization
                # Prune any path that had an unnecessary wait
                assert (
                    self.state[minute].buyOrder
                    != BuyOrder.UNINITIALIZED
                )
                if (
                    self.state[minute].buyOrder != BuyOrder.BUY_NONE
                    and self.state[minute - 1].buyOrder
                    == BuyOrder.BUY_NONE
                    and self.state[minute - 1].canBuy(
                        self.state[minute].buyOrder
                    )
                ):
                    # continue to instead skip this path but try the next adjacent one
                    break

                if verbose:
                    print(
                        "Have"
                        f" {self.state[minute].resources.ore} ore,"
                        f" {self.state[minute].resources.clay} clay,"
                        f" {self.state[minute].resources.obsidian} obsidian,"
                        f" {self.state[minute].resources.geode} geode"
                    )

                # Subtract the money for buy order
                match self.state[minute].buyOrder:
                    case BuyOrder.BUY_ORE:
                        self.state[
                            minute + 1
                        ].resources.ore -= self.oreRobotCost
                        if verbose:
                            print(
                                f"Spend {self.oreRobotCost} ore to"
                                " start building a ore-collecting"
                                " robot."
                            )
                    case BuyOrder.BUY_CLAY:
                        self.state[
                            minute + 1
                        ].resources.ore -= self.clayRobotCost
                        if verbose:
                            print(
                                f"Spend {self.clayRobotCost} ore to"
                                " start building a clay-collecting"
                                " robot."
                            )
                    case BuyOrder.BUY_OBSIDIAN:
                        self.state[
                            minute + 1
                        ].resources.ore -= self.obsidianRobotCost[0]
                        self.state[
                            minute + 1
                        ].resources.clay -= self.obsidianRobotCost[1]
                        if verbose:
                            print(
                                "Spend"
                                f" {self.obsidianRobotCost[0]} ore"
                                " and"
                                f" {self.obsidianRobotCost[1]} clay"
                                " to start building a"
                                " obsidian-collecting robot."
                            )
                    case BuyOrder.BUY_GEODE:
                        self.state[
                            minute + 1
                        ].resources.ore -= self.geodeRobotCost[0]
                        self.state[
                            minute + 1
                        ].resources.obsidian -= self.geodeRobotCost[1]
                        if verbose:
                            print(
                                f"Spend {self.geodeRobotCost[0]} ore"
                                f" and {self.geodeRobotCost[1]} clay"
                                " to start building a geode-cracking"
                                " robot."
                            )
                    case BuyOrder.BUY_NONE:
                        pass
                    case _:
                        assert False

                assert self.state[minute + 1].resources.ore >= 0
                assert self.state[minute + 1].resources.clay >= 0
                assert self.state[minute + 1].resources.obsidian >= 0
                assert self.state[minute + 1].resources.geode >= 0

                # Let the robots do their thing
                if self.state[minute].robots.ore:
                    self.state[
                        minute + 1
                    ].resources.ore += self.state[minute].robots.ore
                    if verbose:
                        print(
                            f"{self.state[minute].robots.ore} ore-collecting"
                            " robot collects"
                            f" {self.state[minute].robots.ore} ore;"
                            " you now have"
                            f" {self.state[minute + 1].resources.ore} ore."
                        )
                if self.state[minute].robots.clay:
                    self.state[
                        minute + 1
                    ].resources.clay += self.state[minute].robots.clay
                    if verbose:
                        print(
                            f"{self.state[minute].robots.clay} clay-collecting"
                            " robot collects"
                            f" {self.state[minute].robots.clay} clay;"
                            " you now have"
                            f" {self.state[minute + 1].resources.clay} clay."
                        )
                if self.state[minute].robots.obsidian:
                    self.state[
                        minute + 1
                    ].resources.obsidian += self.state[
                        minute
                    ].robots.obsidian
                    if verbose:
                        print(
                            f"{self.state[minute].robots.obsidian} obsidian-collecting"
                            " robot collects"
                            f" {self.state[minute].robots.obsidian} obsidian;"
                            " you now have"
                            f" {self.state[minute + 1].resources.obsidian} obsidian."
                        )
                if self.state[minute].robots.geode:
                    self.state[
                        minute + 1
                    ].resources.geode += self.state[
                        minute
                    ].robots.geode
                    if verbose:
                        print(
                            f"{self.state[minute].robots.geode} geode-cracking"
                            " robot collects"
                            f" {self.state[minute].robots.geode} geode;"
                            " you now have"
                            f" {self.state[minute + 1].resources.geode} geode."
                        )

                # Add the robots for the buy order
                match self.state[minute].buyOrder:
                    case BuyOrder.BUY_ORE:
                        self.state[minute + 1].robots.ore += 1
                        if verbose:
                            print(
                                "The new ore-collecting robot is"
                                " ready; you now have"
                                f" {self.state[minute + 1].robots.ore} of"
                                " them."
                            )
                    case BuyOrder.BUY_CLAY:
                        self.state[minute + 1].robots.clay += 1
                        if verbose:
                            print(
                                "The new clay-collecting robot is"
                                " ready; you now have"
                                f" {self.state[minute + 1].robots.clay} of"
                                " them."
                            )
                    case BuyOrder.BUY_OBSIDIAN:
                        self.state[minute + 1].robots.obsidian += 1
                        if verbose:
                            print(
                                "The new obsidian-collecting robot"
                                " is ready; you now have"
                                f" {self.state[minute + 1].robots.obsidian} of"
                                " them."
                            )
                    case BuyOrder.BUY_GEODE:
                        self.state[minute + 1].robots.geode += 1
                        if verbose:
                            print(
                                "The new geode-cracking robot is"
                                " ready; you now have"
                                f" {self.state[minute + 1].robots.geode} of"
                                " them."
                            )
                    case BuyOrder.BUY_NONE:
                        pass
                    case _:
                        assert False

            if verbose:
                print("\n**** Setting up next simulation ****")
            lastState = self.state.pop()
            statesSeen += 1
            best = self.recordProgress(
                best, statesSeen, strategy, lastState
            )

            if strategy is None:
                while True:
                    if len(self.state) == 0:
                        return (
                            best,
                            int(time.time() - startTime),
                            statesSeen,
                        )
                    else:
                        if verbose:
                            print(f"Popping {len(self.state)}")
                        poppedState = self.state.pop()
                    validOrder = poppedState.nextOrder()
                    if validOrder is True:
                        if verbose:
                            print(
                                "Order is valid so continuing to sim"
                            )
                        self.state.append(poppedState)
                        break
            else:
                self.initState()

    def recordProgress(
        self,
        previousBest: int,
        statesSeen: int,
        strategy: Optional[tuple[int, ...]],
        lastState: State,
    ) -> int:
        ALWAYS_PRINT = False
        NEVER_PRINT = False
        # printChance = 100
        # printChance = 1000
        # printChance = 10000
        printChance = 100000
        shouldPrint = ALWAYS_PRINT or random.randint(
            1, printChance
        ) > (printChance - 1)

        if strategy is not None:
            shouldPrint = True

        if NEVER_PRINT is True:
            shouldPrint = False

        best = previousBest
        newBestStar = " "
        if lastState.resources.geode > previousBest:
            best = lastState.resources.geode
            newBestStar = "*"
            if NEVER_PRINT is not True:
                shouldPrint = True

        if shouldPrint:
            print(
                (
                    rf"\[{self.name}]\[{lastState.resources.geode:2}/{best:2}{newBestStar}] "
                ),
                end="",
            )

        if shouldPrint:
            for s in self.state:
                match s.buyOrder:
                    case BuyOrder.BUY_ORE:
                        print("[green]o[/green]", end="")
                    case BuyOrder.BUY_CLAY:
                        print("[yellow]c[/yellow]", end="")
                    case BuyOrder.BUY_OBSIDIAN:
                        print("[red]b[/red]", end="")
                    case BuyOrder.BUY_GEODE:
                        print("[blue]g[/blue]", end="")
                    case BuyOrder.BUY_NONE:
                        print(".", end="")
                    case _:
                        assert False
            for _ in range(len(self.state), self.totalMinutes):
                print("?", end="")
            statesSeenM = convertToMillion(statesSeen)
            print(
                (
                    f" {lastState.robots.ore:2}[green]o[/green],"
                    f" {lastState.robots.clay:2}[yellow]c[/yellow],"
                    f" {lastState.robots.obsidian:2}[red]b[/red],"
                    f" {lastState.robots.geode:2}[blue]g[/blue]"
                    f" ({statesSeenM})"
                ),
                end="",
            )
            if strategy is not None:
                print(
                    f" strat=(o={strategy[0]}, c={strategy[1]},"
                    f" b={strategy[2]})"
                )
            else:
                print(" strat=DFS")
            pass
            if strategy is not None:
                pass
        return best

    def executeBuyOrderStrategy(
        self, strategy: Optional[tuple[int, ...]], minute: int
    ) -> None:
        thisState = self.state[minute]
        if strategy is None:
            if thisState.buyOrder == BuyOrder.UNINITIALIZED:
                nextOrderValid = thisState.nextOrder()
                assert nextOrderValid
        else:
            targetOre = strategy[0]
            targetClay = strategy[1]
            targetObsidian = strategy[2]

            if thisState.canBuy(BuyOrder.BUY_GEODE):
                thisState.buyOrder = BuyOrder.BUY_GEODE
            elif (
                thisState.robots.obsidian < targetObsidian
                and thisState.canBuy(BuyOrder.BUY_OBSIDIAN)
            ):
                thisState.buyOrder = BuyOrder.BUY_OBSIDIAN
            elif (
                thisState.robots.clay < targetClay
                and thisState.canBuy(BuyOrder.BUY_CLAY)
            ):
                thisState.buyOrder = BuyOrder.BUY_CLAY
            elif (
                thisState.robots.ore < targetOre
                and thisState.canBuy(BuyOrder.BUY_ORE)
            ):
                thisState.buyOrder = BuyOrder.BUY_ORE
            else:
                thisState.buyOrder = BuyOrder.BUY_NONE

        assert thisState.buyOrder != BuyOrder.UNINITIALIZED


def solve(
    lines: list[str],
    name: str,
    part1: bool,
    minutes: int,
    blueprints: Optional[int],
    solution: int,
) -> None:
    patternStr = (
        r"Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay"
        r" robot costs (\d+) ore. Each obsidian robot costs (\d+) ore"
        r" and (\d+) clay. Each geode robot costs (\d+) ore and (\d+)"
        r" obsidian."
    )
    pattern = re.compile(patternStr)

    if part1:
        calculated = 0
    else:
        calculated = 1

    statesExploredTotal = 0
    elapsedTimeTotal = 0

    # Read in data
    if blueprints:
        lines = lines[0:blueprints]
    iTotal = len(lines)
    for i, line in enumerate(lines, start=1):
        m = pattern.match(line)
        assert m is not None
        b = Blueprint(
            name=f"{name}-{m.group(1)}/{iTotal}",
            minutes=minutes,
            oreRobotCost=m.group(2),
            clayRobotCost=m.group(3),
            obsidianRobotCost=m.group(4, 5),
            geodeRobotCost=m.group(6, 7),
        )

        assert m

        print(
            f"\nSimulating blueprint {i}/{iTotal} for"
            f" {minutes} minutes..."
        )
        best, elapsedTime, statesExplored = b.sim()
        elapsedTimeTotal += elapsedTime
        statesExploredTotal += statesExplored

        print(f"=> Received best geode count of {best}")
        if part1:
            ql = best * i
            print(f"=> Quality level is {ql}")
            calculated += ql
        else:
            calculated *= best
        print(f"=> Runtime: {elapsedTime:.1f} seconds")
        print(
            f"=> States explored: {convertToMillion(statesExplored)}"
        )

    print()
    print(f"Done running {iTotal} blueprints")
    print(f"Calculated solution:  {calculated}")
    if solution:
        print(f"=> Expected solution: {solution}")
    assert solution is None or calculated == solution

    print()
    print("Stats")
    print(f"=> Runtime: {elapsedTimeTotal:.1f} seconds")
    print(
        f"=> States explored: {convertToMillion(statesExploredTotal)}"
    )


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day19-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    name="p1-mini",
    part1=True,
    minutes=24,
    blueprints=1,
    solution=9,
)

with open("day19-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    name="p1-test",
    part1=True,
    minutes=24,
    blueprints=None,
    solution=33,
)

with open("day19-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    name="p1",
    part1=True,
    minutes=24,
    blueprints=None,
    solution=1413,
)

# Part 2
with open("day19-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    name="p2",
    part1=False,
    minutes=32,
    blueprints=2,
    solution=56 * 62,
)

with open("day19-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    name="p2",
    part1=False,
    minutes=32,
    blueprints=3,
    solution=21080,
)
