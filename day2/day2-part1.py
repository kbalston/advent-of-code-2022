#!/usr/bin/env python3
import os

os.chdir(os.path.realpath(os.path.dirname(__file__)))
with open("day2-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()

score = 0
for line in lines:
    theirMove, myMove= line.split()
    theirMove = ord(theirMove) - ord("A") + 1
    myMove = ord(myMove) - ord("X") + 1
    # 1 -> rock
    # 2 -> paper
    # 3 -> scissors
    if myMove == theirMove:
        # Tie
        score += 3 + myMove
        print(f"{myMove} vs {theirMove} -> Tie")
    elif myMove == 1 and theirMove == 3 or \
         myMove == 2 and theirMove == 1 or \
         myMove == 3 and theirMove == 2:
        # Win
        score += 6 + myMove
        print(f"{myMove} vs {theirMove} -> Win")
    else:
        score += myMove
        print(f"{myMove} vs {theirMove} -> Lose")

    # print(myMove)
    # print(theirMove)
print(score)
assert(score != 10933)
