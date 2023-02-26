#!/usr/bin/env python3

from __future__ import annotations
from collections import defaultdict, deque
from dataclasses import dataclass

import os
import re
from typing import Optional, Tuple


class Room:
    def __init__(
        self, name: str, rate: int, connections: list[str]
    ) -> None:
        self.name = name
        self.rate = rate
        self.connectionsStr = connections
        self.connections: list[Room] = []

    def __repr__(self) -> str:
        return f"Room{{{self.name}@{self.rate:>02}}}"


def findDistance(src: Room, dest: Room, verbose: bool = False) -> int:
    @dataclass
    class State:
        room: Room
        distance: int

    assert src != dest

    states: deque[State] = deque()
    states.appendleft(State(room=src, distance=0))

    while len(states) > 0:
        state = states.pop()
        nextDistance = state.distance + 1
        if dest in state.room.connections:
            # Found it!
            if verbose:
                print(
                    f"Distance from {src} to {dest} is"
                    f" {state.distance}"
                )
            return nextDistance

        for next in state.room.connections:
            states.appendleft(State(room=next, distance=nextDistance))
    else:
        assert False, f"Unable to find a path from {src} to {dest}"


def findDistances(
    rooms: dict[str, Room]
) -> dict[Room, dict[Room, int]]:
    distances: dict[Room, dict[Room, int]] = {}
    for src in rooms.values():
        for dest in rooms.values():
            if src == dest:
                continue
            if src.name != "AA" and src.rate == 0:
                continue
            if dest.rate == 0:
                continue
            dist = findDistance(src, dest)
            if src not in distances:
                distances[src] = {}
            # Add one to the distance to account for opening the valve
            distances[src][dest] = dist + 1

    return distances


def reconcileConnections(rooms: dict[str, Room]) -> None:
    for room in rooms.values():
        for connectionStr in room.connectionsStr:
            room.connections.append(rooms[connectionStr])


def findBestPath(
    start: Room,
    distances: dict[Room, dict[Room, int]],
    minutes: int,
    actors: int,
    alreadyOpen: frozenset[Room],
    verbose: bool = True,
) -> Tuple[int, Optional[list[Room]]]:
    @dataclass
    class State:
        timeRemaining: int
        totalPressure: int
        path: list[Room]

    assert actors in (1, 2)

    current: Room = start
    states = list()
    states.append(
        State(timeRemaining=minutes, totalPressure=0, path=[start])
    )
    otherCache = dict()
    stats: defaultdict[str, int] = defaultdict(int)

    bestPressure = 0
    bestPath = None
    while len(states):
        state = states.pop()
        current = state.path[-1]
        for next in distances[current]:
            if next in state.path:
                continue
            if next in alreadyOpen:
                continue
            thisTime = distances[current][next]
            nextTimeRemaining = state.timeRemaining - thisTime
            if nextTimeRemaining < 0:
                continue
            thisPressure = (
                state.totalPressure + nextTimeRemaining * next.rate
            )
            nextTotalPressure = thisPressure
            nextPath = list()
            nextPath.extend(state.path)
            nextPath.append(next)
            # Now check the elephant's path
            if actors == 2:
                otherAlreadyOpen = frozenset(nextPath)
                if otherAlreadyOpen not in otherCache:
                    otherCache[otherAlreadyOpen] = findBestPath(
                        start=start,
                        distances=distances,
                        minutes=minutes,
                        actors=1,
                        alreadyOpen=otherAlreadyOpen,
                        verbose=False,
                    )
                    stats["otherCacheMisses"] += 1
                else:
                    stats["otherCacheHits"] += 1
                otherPressure, otherPath = otherCache[
                    otherAlreadyOpen
                ]
                nextTotalPressure += otherPressure

            if nextTotalPressure > bestPressure:
                bestPressure = nextTotalPressure
                bestPath = nextPath.copy()
                if verbose:
                    print(f"New best pressure of {bestPressure}")
                    print(
                        f" + [{thisPressure:>4}]"
                        f" {nextPath} (timeRemaining={nextTimeRemaining})"
                    )
                if actors == 2:
                    print(f" + [{otherPressure:>4}] {otherPath} ")
            nextState = State(
                timeRemaining=nextTimeRemaining,
                totalPressure=thisPressure,
                path=nextPath,
            )
            stats["states"] += 1
            states.append(nextState)
    if verbose:
        print(f"Best is {bestPressure}")
    return bestPressure, bestPath


def solve(
    lines: list[str], minutes: int, actors: int, solution: int
) -> None:
    # Read in data
    pattern = re.compile(
        r"Valve (\w+) has flow rate=(\d+); tunnels* leads* to valves*"
        r" ([ ,\w]+)"
    )
    rooms = dict()
    for line in lines:
        m = re.match(pattern, line)
        assert m
        name = m.group(1)
        rate = int(m.group(2))
        connections = m.group(3).split(", ")
        room = Room(name, rate, connections)
        assert room.name not in rooms
        rooms[room.name] = room

    reconcileConnections(rooms)

    # Calculate distances between rooms
    distances = findDistances(rooms)

    bestPressure, bestPaths = findBestPath(
        start=rooms["AA"],
        distances=distances,
        minutes=minutes,
        alreadyOpen=frozenset(),
        actors=actors,
    )

    print(
        f"Received a best pressure of {bestPressure} via {bestPaths}"
    )

    if solution is not None:
        print(f"=> Expecting {solution}")
        assert bestPressure == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day16-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    minutes=30,
    actors=1,
    solution=1651,
)

with open("day16-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    minutes=30,
    actors=1,
    solution=1584,
)

# Part 2
with open("day16-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    minutes=26,
    actors=2,
    solution=1707,
)

with open("day16-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    minutes=26,
    actors=2,
    solution=2052,
)
