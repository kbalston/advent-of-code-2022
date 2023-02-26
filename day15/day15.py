#!/usr/bin/env python3

from __future__ import annotations
from collections import defaultdict
import logging

import os
import re
from typing import Optional, Tuple, cast

# There's a lot of output for this puzzle solution,
# so make the output configurable via a logger
logging.basicConfig(format="%(message)s", level=logging.INFO)


def distance(sensor: Tuple[int, int], beacon: Tuple[int, int]) -> int:
    return abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])


def setPosWithinDist(
    sensor: Tuple[int, int], dist: int, grid: SequenceTable
) -> None:
    for y in range(sensor[1] - dist, sensor[1] + dist + 1):
        distY = abs(y - sensor[1])
        distX = dist - distY
        minX = sensor[0] - distX
        maxX = sensor[0] + distX
        grid.set(minX=minX, maxX=maxX, y=y)
        logging.debug(
            f"setPosWithinDist -> setting {minX}<->{maxX} @ {y}"
        )


class SequenceTable:
    def __init__(
        self,
        clampX: Optional[Tuple[int, int]] = None,
        clampY: Optional[Tuple[int, int]] = None,
    ) -> None:
        self.storage: defaultdict[int, list[Tuple[int, int]]] = (
            defaultdict(list)
        )
        self.beaconOrSensor: dict[Tuple[int, int], bool] = {}
        self.clampX = clampX
        self.clampY = clampY

    def set(self, minX: int, maxX: int, y: int) -> None:
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
        logging.debug(
            f"* Looking to insert ({minX}, {maxX}) into existing"
            f" bounds of {seq} @ y={y}"
        )
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
                logging.debug(
                    f"** Extending previous bounds of {prev} to"
                    f" ({minX}, {maxX}) @ y={y}"
                )
                if minX != prevMinX or maxX != prevMaxX:
                    seq.remove(prev)
                    self.set(minX, maxX, y)
                else:
                    assert False, "Expected to extend range"
                break
        else:
            # Completely new
            logging.debug(
                f"** Adding new bounds of {minX},{maxX} @ y={y}"
            )
            seq.append((minX, maxX))

    def setBeaconOrSensor(self, pos: Tuple[int, int]) -> None:
        self.beaconOrSensor[pos] = True

    def countAtY(self, y: int) -> int:
        count = 0
        seq = self.storage[y]
        for minX, maxX in seq:
            for x in range(minX, maxX + 1):
                if self.beaconOrSensor.get((x, y), None):
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
                logging.info(f"Found empty spot at {x}, {y}")
                logging.info(f"=> Tuning is {tuning}")
                return tuning
        assert False


def solve(
    lines: list[str],
    part1: bool,
    clampX: Optional[Tuple[int, int]],
    clampY: Optional[Tuple[int, int]],
    solution: int,
) -> None:
    # Read in data
    grid = SequenceTable(clampX=clampX, clampY=clampY)
    pattern = re.compile(
        r"Sensor at x=([-\d]+), y=([-\d]+): "
        r"closest beacon is at x=([-\d]+), y=([-\d]+)"
    )
    sensorTotal = len(lines)
    for sensorI, line in enumerate(lines, start=1):
        logging.info("#" * 20)
        logging.info(line)
        m = re.match(pattern, line)
        assert m
        logging.info(m.groups())
        assert len(m.groups()) == 4
        # mypy is unable to automatically infer the size of these tuples
        sensor = cast(
            Tuple[int, int], tuple(int(x) for x in m.group(1, 2))
        )
        beacon = cast(
            Tuple[int, int], tuple(int(x) for x in m.group(3, 4))
        )
        logging.info(
            f"Sensor {sensorI:>2}/{sensorTotal:>2} is at {sensor};"
            f" beacon is at {beacon}"
        )
        dist = distance(sensor, beacon)
        logging.info(f"=> dist: {dist}")
        setPosWithinDist(sensor, dist, grid)
        grid.setBeaconOrSensor(beacon)
        grid.setBeaconOrSensor(sensor)
    logging.info("Calculating solution...")
    if part1:
        assert clampY is not None
        assert clampY[0] == clampY[1]
        calculated = grid.countAtY(clampY[0])
    else:  # Part2
        calculated = grid.findTuningFrequency()

    logging.info(f"Calculated: {calculated}")
    if solution is not None:
        logging.info(f"=> Expecting {solution}")
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
