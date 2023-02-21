#!/usr/bin/env python3

import os
import re
from pathlib import Path
import sys


class FilesystemItem:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.size = 0
        self.totalSize = 0
        self.children: list[FilesystemItem] = []

    def __repr__(self) -> str:
        return f"FilesystemItem{{{self.path.resolve()}, {self.size}}}"

    def calculateSize(self) -> int:
        self.totalSize = self.size
        for child in self.children:
            self.totalSize += child.calculateSize()
        return self.totalSize

    def sumUnderLimit(self, limit: int) -> int:
        sum = 0
        # Add self
        if self.totalSize < limit:
            sum += self.totalSize
        # Add children recursively
        for child in self.children:
            sum += child.sumUnderLimit(limit)
        return sum

    def findDelete(self, targetSize: int) -> int:
        best = sys.maxsize
        # Check self
        if self.totalSize >= targetSize and (self.totalSize < best):
            best = self.totalSize
        # Check children recursively
        for child in self.children:
            best = min(best, child.findDelete(targetSize))
        return best


def solve(
    lines: list[str],
    limit: int,
    solutionPart1: int,
    solutionPart2: int,
) -> None:
    sum = 0
    currentCommand = None
    currentCommandOption = None
    root = FilesystemItem(Path("/"))
    currentWorkingDirectory = root
    seen = {root.path: root}
    for line in lines:
        print(f"\nLine: '{line}'")
        matchCommand = re.match(r"^\$ (\S+)\s*(\S*)", line)
        if matchCommand:
            print(
                f"=> Detected new command: {matchCommand.groups()} @"
                f" {currentWorkingDirectory.path}"
            )
            currentCommand = matchCommand.group(1)
            if matchCommand.group(2):
                currentCommandOption = matchCommand.group(2)
            else:
                currentCommandOption = None
            print(f"=> {currentCommand} {currentCommandOption}")
            if currentCommand == "cd":
                assert currentCommandOption is not None
                targetPath = Path(currentCommandOption)
                if targetPath.is_absolute():
                    newPath = targetPath
                else:
                    newPath = (
                        currentWorkingDirectory.path / targetPath
                    )
                    newPath = newPath.resolve()
                if newPath in seen:
                    # We've seen this one before
                    nextWorkingDirectory = seen[newPath]
                else:
                    # We haven't seen this one before, allocate it
                    nextWorkingDirectory = FilesystemItem(newPath)
                    seen[newPath] = nextWorkingDirectory
                if (
                    nextWorkingDirectory.path.is_relative_to(
                        currentWorkingDirectory.path
                    )
                    and currentWorkingDirectory.path
                    != nextWorkingDirectory.path
                ):
                    print(
                        f"{currentWorkingDirectory} is a parent of"
                        f" {nextWorkingDirectory}"
                    )
                    currentWorkingDirectory.children.append(
                        nextWorkingDirectory
                    )
                currentWorkingDirectory = nextWorkingDirectory
                del nextWorkingDirectory
                print(
                    "=> Changed directory to"
                    f" {currentWorkingDirectory.path}"
                )
            elif currentCommand == "ls":
                pass
            else:
                assert False
        else:
            print(
                "=> Detected output from previous command"
                f" ({currentCommand} {currentCommandOption})"
            )
            if currentCommand == "cd":
                assert False, "Should have no output"
            elif currentCommand == "ls":
                matchOutput = re.match(r"^(\S+)\s+(\S+)", line)
                assert matchOutput is not None
                size = matchOutput.group(1)
                if size == "dir":
                    size = 0
                else:
                    size = int(size)
                target = matchOutput.group(2)
                print(f"=> Target: {target}; size: {size}")
                currentWorkingDirectory.size += size
            else:
                assert False

    print("\nCalculating solutions...")
    diskTotal = 70000000
    diskTargetFree = 30000000
    root.calculateSize()
    diskCurrentFree = diskTotal - root.totalSize
    targetDeletionSize = diskTargetFree - diskCurrentFree

    print("{:>20}: {:>10}".format("diskTotal", diskTotal))
    print("{:>20}: {:>10}".format("diskTargetFree", diskTargetFree))

    print("{:>20}: {:>10}".format("diskCurrentUsed", root.totalSize))
    print("{:>20}: {:>10}".format("diskCurrentFree", diskCurrentFree))
    print(
        "{:>20}: {:>10}".format(
            "targetDeletionSize", targetDeletionSize
        )
    )

    # Part 1
    sum = root.sumUnderLimit(limit)
    print(f"Part 1: sum of folders under {limit} is {sum}")
    assert solutionPart1 is None or solutionPart1 == sum

    # Part 2
    smallestToDelete = root.findDelete(targetSize=targetDeletionSize)
    print(
        "Part 2: size of smallest folder we can delete is"
        f" {smallestToDelete}"
    )
    assert solutionPart2 is None or solutionPart2 == smallestToDelete


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day7-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines, limit=100000, solutionPart1=95437, solutionPart2=24933642
)

with open("day7-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines, limit=100000, solutionPart1=1886043, solutionPart2=3842121
)
