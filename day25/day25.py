#!/usr/bin/env python3

from __future__ import annotations
import os


def numberToBaseReversed(number: int, base: int = 5) -> list[int]:
    assert number > 0
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return digits


def convertOneBaseFiveDigitToSnafu(
    digitBaseFive: int,
) -> tuple[str, int]:
    match digitBaseFive:
        case 0 | 1 | 2:
            digitSnafu = str(digitBaseFive)
            carry = 0
        case 3:
            digitSnafu = "="
            carry = 1
        case 4:
            digitSnafu = "-"
            carry = 1
        case _:
            assert False
    return digitSnafu, carry


def toSnafu(numberBaseTen: int) -> str:
    numberBaseFive = numberToBaseReversed(numberBaseTen, 5)

    snafuDigitsReversed = list()
    carry = 0
    for n in numberBaseFive:
        n2, carry = convertOneBaseFiveDigitToSnafu(n + carry)
        snafuDigitsReversed.append(n2)
    if carry:
        n2, carry = convertOneBaseFiveDigitToSnafu(carry)
        snafuDigitsReversed.append(n2)

    snafuDigitsReversed.reverse()
    snafuDigits = "".join(snafuDigitsReversed)

    return snafuDigits


def toDec(input: str) -> int:
    number = 0
    for place, c in enumerate(input[::-1]):
        match c:
            case "0" | "1" | "2":
                c2 = int(c)
            case "=":
                c2 = -2
            case "-":
                c2 = -1
            case _:
                assert False
        thisNumber = 5**place * c2
        number += thisNumber

    return number


def solve(
    lines: list[str], solutionSnafu: str, solutionDec: int
) -> None:
    s = 0

    for line in lines:
        dec = toDec(line)
        s += dec
        print(f"{line} converts to {dec}")

    print()
    print(f"Sum of numbers is {s}")
    print(f"=> Expecting      {solutionDec}")

    s2 = toSnafu(s)
    print()
    print(f"Sum converted to snafu is {s2}")
    print(f"=> Expecting              {solutionSnafu}")

    assert s == solutionDec
    assert s2 == solutionSnafu


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day24-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionDec=4890,
    solutionSnafu="2=-1=0",
)

with open("day24-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    solutionDec=30535047052797,
    solutionSnafu="2=001=-2=--0212-22-2",
)

# No part 2 in this one
