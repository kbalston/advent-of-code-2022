#!/usr/bin/env python3

from __future__ import annotations
from collections import deque

import os
import re
from typing import Any, Optional, Tuple, Union
import logging


# There's a lot of output for this puzzle solution,
# so make the output configurable via a logger
logging.basicConfig(format="%(message)s", level=logging.WARNING)


class Monkey:
    def __init__(
        self,
        number: int,
        items: list[int],
        op: str,
        opParam: Union[int, str],
        testOp: int,
        ifTrue: int,
        ifFalse: int,
    ) -> None:
        self.number = number
        self.items = deque(items)
        self.op = op
        self.opParam = opParam
        self.testOp = testOp
        self.ifTrue = ifTrue
        self.ifFalse = ifFalse

        self.inspections = 0

    def __str__(self) -> str:
        return f"Monkey{self.number}{{{list(self.items)}}}]"

    def inspect(self, item: int, worryReducer: Optional[int]) -> int:
        self.inspections += 1
        logging.info(
            f"  Monkey inspects an item with a worry level of {item}."
        )
        match self.op:
            case "*":
                # Type narrowing to satisfy mypy
                if isinstance(self.opParam, str):
                    assert self.opParam == "old"
                    item *= item
                else:
                    item *= self.opParam
                logging.debug(
                    "    Worry level is multiplied by"
                    f" {self.opParam} to {item}."
                )
            case "+":
                # Type narrowing to satisfy mypy
                if isinstance(self.opParam, str):
                    assert self.opParam == "old"
                    item += item
                else:
                    item += self.opParam
                logging.debug(
                    f"    Worry level increases by {self.opParam} to"
                    f" {item}."
                )
            case _:
                assert False
        if worryReducer is not None:
            item %= worryReducer
        return item

    def test(self, item: int) -> Tuple[bool, int]:
        if item % self.testOp == 0:
            logging.debug(
                "    Current worry level is divisible by"
                f" {self.testOp}."
            )
            return True, item
        else:
            logging.debug(
                "    Current worry level is not divisible by"
                f" {self.testOp}."
            )
            return False, item


def solve(
    lines: list[str], rounds: int, part1: bool, solution: int
) -> None:
    patternsStr = (
        r"Monkey (\d+):",
        r"  Starting items: ([\d, ]+)",
        r"  Operation: new = old ([+*]) (.*)",
        r"  Test: divisible by (\d+)",
        r"    If true: throw to monkey (\d+)",
        r"    If false: throw to monkey (\d+)",
        None,
    )
    patterns = list(
        re.compile(pattern) if pattern else None
        for pattern in patternsStr
    )
    # TODO: It would be better if we could narrow the `Any` here
    matches: list[Union[str, Tuple[Union[str, Any], ...]]] = list()
    monkeys: list[Monkey] = list()

    # Force an empty line at the end
    if lines[-1] != "":
        lines.append("")
    # Read in data
    for i, line in enumerate(lines):
        logging.warning(line)
        pattern: Optional[re.Pattern[str]] = patterns[
            i % len(patterns)
        ]
        if pattern is not None:
            m = pattern.match(line)
            assert m, f"{pattern} did not match against {line}"
            if len(m.groups()) > 1:
                matches.append(m.groups())
            else:
                matches.append(m.group(1))
        else:
            number, items, operation, test, ifTrue, ifFalse = matches
            if operation[1] == "old":
                pass
            else:
                operation = operation[0], int(operation[1])
            logging.warning(operation)
            # Type narrowing to satisfy mypy
            assert isinstance(number, str)
            assert isinstance(items, str)
            assert isinstance(test, str)
            assert isinstance(ifTrue, str)
            assert isinstance(ifFalse, str)
            monkey = Monkey(
                number=int(number),
                items=[int(item) for item in items.split(", ")],
                op=operation[0],
                opParam=operation[1],
                testOp=int(test),
                ifTrue=int(ifTrue),
                ifFalse=int(ifFalse),
            )
            monkeys.append(monkey)
            matches.clear()
    assert len(matches) == 0

    for monkey in monkeys:
        logging.warning(monkey)

    if part1:
        worryReducer = None
    else:
        worryReducer = 1
        for monkey in monkeys:
            worryReducer *= monkey.testOp

    for round in range(rounds):
        logging.warning(f"=== Simulating round {round}...")

        for monkey in monkeys:
            logging.info(f"Monkey {monkey.number}")
            while monkey.items:
                item = monkey.items.popleft()
                item = monkey.inspect(item, worryReducer)
                if part1:
                    item //= 3
                    logging.info(
                        "    Monkey gets bored with item. Worry"
                        f" level is divided by 3 to {item}."
                    )
                interested, item = monkey.test(item)
                if interested:
                    throwTarget = monkey.ifTrue
                else:
                    throwTarget = monkey.ifFalse
                logging.info(
                    f"    Item with worry level {item} is thrown to"
                    f" monkey {throwTarget}."
                )
                monkeys[throwTarget].items.append(item)

        logging.info(
            f"After round {round}, the monkeys are holding items with"
            " these worry levels:"
        )
        for monkey in monkeys:
            logging.info(f"Monkey {monkey.number}: {monkey.items}")

    for monkey in monkeys:
        logging.warning(
            f"Monkey {monkey.number}: inspected items"
            f" {monkey.inspections} times"
        )

    inspections = [monkey.inspections for monkey in monkeys]
    inspections = sorted(inspections, reverse=True)[0:2]

    monkeyBusiness = inspections[0] * inspections[1]

    logging.info(f"Monkey business: {monkeyBusiness}")
    logging.info(f"=>    Expecting: {solution}")
    assert monkeyBusiness == solution, (
        f"Calculated monkey business was {monkeyBusiness} but"
        f" expected {solution}"
    )


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day11-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=20,
    part1=True,
    solution=10605,
)

with open("day11-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=20,
    part1=True,
    solution=90294,
)

# Part 2
with open("day11-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=10000,
    part1=False,
    solution=2713310158,
)

with open("day11-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    rounds=10000,
    part1=False,
    solution=18170818354,
)
