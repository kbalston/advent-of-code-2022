#!/usr/bin/env python3
import os

os.chdir(os.path.realpath(os.path.dirname(__file__)))
with open("day2-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()

def calculateMyMove(theirMove, endCondition):
    if endCondition == 'Y':
        return theirMove
    elif endCondition == 'Z':
        # Win
        if theirMove == 1:
            return 2
        if theirMove == 2:
            return 3
        if theirMove == 3:
            return 1
    elif endCondition == 'X':
        # Lose
        if theirMove == 1:
            return 3
        if theirMove == 2:
            return 1
        if theirMove == 3:
            return 2
    else:
        assert(False)


score = 0
for line in lines:
    theirMove, endCondition = line.split()
    theirMove = ord(theirMove) - ord("A") + 1
    # 1 -> rock
    # 2 -> paper
    # 3 -> scissors
    # X -> lose
    # Y -> tie
    # Z -> win
    myMove = calculateMyMove(theirMove, endCondition)
    if endCondition == 'Y':
        # Tie
        score += 3 + myMove
        print(f"{myMove} vs {theirMove} -> Tie")
    elif endCondition == 'Z':
        # Win
        score += 6 + myMove
        print(f"{myMove} vs {theirMove} -> Win")
    elif endCondition == 'X':
        # Lose
        score += myMove
        print(f"{myMove} vs {theirMove} -> Lose")
    else:
        assert(False)

    # print(myMove)
    # print(theirMove)
print(score)
assert(score != 10933)
