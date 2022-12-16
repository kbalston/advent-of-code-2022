#!/usr/bin/env python3

from __future__ import annotations
from collections import defaultdict

import os
import re


def distance(sensor, beacon) -> int:
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def setPosWithinDist(sensor, dist, grid: SequenceTable):
    for y in range(sensor[1] - dist, sensor[1] + dist + 1):
        distY = abs(y - sensor[1])
        distX = dist - distY
        minX = sensor[0] - distX
        maxX = sensor[0] + distX
        grid.set(minX=minX, maxX=maxX, y=y)
        # print(f"setPosWithinDist -> setting {minX}<->{maxX} @ {y}")


class SequenceTable:
    def __init__(self, clampX=None, clampY=None) -> None:
        self.storage = defaultdict(list)
        self.beaconOrSensor = dict()
        self.clampX = clampX
        self.clampY = clampY

    # def get(self, x, y) -> bool:
    #     if self.beaconOrSensor.get((x, y), None) is not None:
    #         return None
    #     seq = self.storage[y]
    #     for minX, maxX in seq:
    #         if x >= minX and x <= maxX:
    #             return True
    #     else:
    #         return False

    def set(self, minX, maxX, y) -> None:
        if self.clampY:
            if y < self.clampY[0] or y > self.clampY[1]:
                return
        if self.clampX:
            if maxX < self.clampX[0] or minX > self.clampX[1]:
                return
            if minX < self.clampX[0]:
                minX = self.clampX[0]

            if maxX > self.clampX[1]:
                maxX = self.clampX[1]

        seq = self.storage[y]
        # print(f"* Looking to insert ({minX}, {maxX}) into existing bounds of {seq} @ y={y}")
        for prev in seq:
            (prevMinX, prevMaxX) = prev
            minXWithinPrevRange = (
                minX >= prevMinX and minX <= prevMaxX
            )
            maxXWithinPrevRange = (
                maxX >= prevMinX and maxX <= prevMaxX
            )
            if minXWithinPrevRange and maxXWithinPrevRange:
                # Nothing to do because `prev` is already larger than (`minX`, `maxX`)
                return
            if (
                minXWithinPrevRange
                # Check if new bounds overlap with old ones
                or maxXWithinPrevRange
                # Check if new bounds are adjacent with old ones
                or prevMaxX + 1 == minX
                or maxX + 1 == prevMinX
                # Check if new bounds completely contain old bounds
                or minX <= prevMinX
                and maxX >= prevMaxX
            ):
                if prevMinX < minX:
                    minX = prevMinX
                if prevMaxX > maxX:
                    maxX = prevMaxX
                # print(f"** Extending previous bounds of {prev} to ({minX}, {maxX}) @ y={y}")
                if minX != prevMinX or maxX != prevMaxX:
                    seq.remove(prev)
                    self.set(minX, maxX, y)
                else:
                    assert False, "Expected to extend range"
                break
        else:
            # Completely new
            # print(f"** Adding new bounds of {minX},{maxX} @ y={y}")
            seq.append((minX, maxX))

    def setBeaconOrSensor(self, pos) -> None:
        self.beaconOrSensor[pos] = True

    def countAtY(self, y) -> None:
        count = 0
        seq = self.storage[y]
        for minX, maxX in seq:
            for x in range(minX, maxX + 1):
                if self.beaconOrSensor.get((x, y), None) is not None:
                    # Is beacon or sensor
                    continue
                count += 1
        return count

    def findTuningFrequency(self) -> int:
        for y, seq in self.storage.items():
            assert len(seq) in (1, 2)
            if len(seq) == 2:
                # Found it?
                seq = sorted(seq)
                x = seq[0][1] + 1
                x2 = seq[1][0] - 1
                assert x == x2
                tuning = x * 4000000 + y
                print(f"Found empty spot at {x}, {y}")
                print(f"=> Tuning is {tuning}")
                return tuning
        assert False


def solve(lines, part1, clampX, clampY, solution) -> None:
    # Read in data
    grid = SequenceTable(clampX=clampX, clampY=clampY)
    pattern = re.compile(
        r"Sensor at x=([-\d]+), y=([-\d]+): closest beacon is at"
        r" x=([-\d]+), y=([-\d]+)"
    )
    sensorTotal = len(lines)
    for sensorI, line in enumerate(lines, start=1):
        print("#" * 20)
        print(line)
        m = re.match(pattern, line)
        assert m
        print(m.groups())
        assert len(m.groups()) == 4
        sensor = tuple(int(x) for x in m.group(1, 2))
        beacon = tuple(int(x) for x in m.group(3, 4))
        print(
            f"Sensor {sensorI:>2}/{sensorTotal:>2} is at {sensor};"
            f" beacon is at {beacon}"
        )
        dist = distance(sensor, beacon)
        print(f"=> dist: {dist}")
        setPosWithinDist(sensor, dist, grid)
        grid.setBeaconOrSensor(beacon)
        grid.setBeaconOrSensor(sensor)

        print()
    print("Calculating solution...")
    if part1:
        assert clampY[0] == clampY[1]
        calculated = grid.countAtY(clampY[0])
    else:  # Part2
        calculated = grid.findTuningFrequency()

    print(f"Calculated: {calculated}")
    if solution is not None:
        print(f"=> Expecting {solution}")
        assert calculated == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day15-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    clampX=None,
    clampY=(10, 10),
    solution=26,
)

with open("day15-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    clampX=None,
    clampY=(2000000, 2000000),
    solution=5181556,
)

# Part 2
with open("day15-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    clampX=(0, 20),
    clampY=(0, 20),
    solution=56000011,
)

with open("day15-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    clampX=(0, 4000000),
    clampY=(0, 4000000),
    solution=12817603219131,
)
