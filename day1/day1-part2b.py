#!/usr/bin/env python3
import heapq
import os

os.chdir(os.path.realpath(os.path.dirname(__file__)))
with open("day1-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()

# Initialize variables used for summation
numberOfElvesToTrack = 3
# We'll start with a value of `-1` since
# that should be smaller than any value any elf can carry
allElves = [-1] * numberOfElvesToTrack
thisElf = 0

# Lets make sure we terminate the sequence with
# an empty line so we close out that elf's calories
if lines[-1]:
    lines.append("")

for line in lines:
    if not line:
        print(f"This elf was seen carrying {thisElf:6} calories")
        # We assume that `-1` is smaller than any
        # possible calorie amount
        assert thisElf > 0
        # `heappushpop` will add `thisElf` to `allElves` and pop the smallest value
        heapq.heappushpop(allElves, thisElf)
        thisElf = 0
        continue
    c = int(line)
    thisElf += c

print("Done iterating")
print(f"We have collected data on {len(allElves)} elves")
# Lets make sure we popped off all of those calorie counts
assert len(allElves) >= numberOfElvesToTrack
topThree = sum(allElves)
print(f"The top three elves are carrying a sum of {topThree:6} calories")

# Check against the solution we previously submitted
assert topThree == 209603
