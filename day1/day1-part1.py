#!/usr/bin/env python3
import os

os.chdir(os.path.realpath(os.path.dirname(__file__)))
with open("day1-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()

# Initialize variables used for summation
maxElf = 0
thisElf = 0

# @@@SNIPSTART day1-part1-input-termination
# Lets make sure we terminate the sequence with
# an empty line so we close out that elf's calories
if lines[-1]:
    lines.append("")
# @@@SNIPEND

# @@@SNIPSTART day1-part1-main
for line in lines:
    if not line:
        print(f"This elf was seen carrying {thisElf:6} calories")
        maxElf = max(maxElf, thisElf)
        print(
            "The elf seen carrying the most calories so far was"
            f" carrying {maxElf:6} calories"
        )
        thisElf = 0
        print()
        continue
    c = int(line)
    thisElf += c
    print(
        f"This elf is carrying an item of food of {c:5} calories, for"
        f" a total of {thisElf:6} calories so far"
    )
# @@@SNIPEND

print("Done iterating")
print(
    "The elf seen carrying the most calories was carrying"
    f" {maxElf:6} calories"
)

# Check against the solution we previously submitted
assert maxElf == 71506
