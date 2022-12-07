#!/usr/bin/env python3

import os
import re
from collections import deque
from pathlib import Path
import sys


class FilesystemItem:
    def __init__(self, path) -> None:
        self.path = path
        self.size = 0
        self.totalSize = None
        self.children = []

    def __repr__(self) -> str:
        return f"FilesystemItem{{{self.path.resolve()}, {self.size}}}"

    def calculateSize(self) -> int:
        self.totalSize = self.size
        for child in self.children:
            self.totalSize += child.calculateSize()
        return self.totalSize

    def sumUnderLimit(self, limit) -> int:
        sum = 0
        # Add self
        if self.totalSize < limit:
            sum += self.totalSize
        # Add children recursively
        for child in self.children:
            sum += child.sumUnderLimit(limit)
        return sum

    def findDelete(self, targetSize) -> int:
        best = sys.maxsize
        # Check self
        if self.totalSize >= targetSize and (self.totalSize < best):
            best = self.totalSize
        # Check children recursively
        for child in self.children:
            best = min(best, child.findDelete(targetSize))
        return best


def solve(lines, limit=100000, solutionPart1=None, solutionPart2=None) -> None:
    sum = 0
    currentCommand = None
    currentCommandOption = None
    root = FilesystemItem(Path("/"))
    currentWorkingDirectory = root
    seen = {root.path: root}
    for line in lines:
        print(f"\nLine: '{line}'")
        matchCommand = re.match("^\$ (\S+)\s*(\S*)", line)
        if matchCommand:
            print(
                f"=> Detected new command: {matchCommand.groups()} @ {currentWorkingDirectory.path}"
            )
            currentCommand = matchCommand.group(1)
            if matchCommand.group(2):
                currentCommandOption = matchCommand.group(2)
            else:
                currentCommandOption = None
            print(f"=> {currentCommand} {currentCommandOption}")
            if currentCommand == "cd":
                targetPath = Path(currentCommandOption)
                if targetPath.is_absolute():
                    newPath = targetPath
                else:
                    newPath = currentWorkingDirectory.path / targetPath
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
                    and currentWorkingDirectory.path != nextWorkingDirectory.path
                ):
                    print(
                        f"{currentWorkingDirectory} is a parent of {nextWorkingDirectory}"
                    )
                    currentWorkingDirectory.children.append(nextWorkingDirectory)
                currentWorkingDirectory = nextWorkingDirectory
                del nextWorkingDirectory
                print(f"=> Changed directory to {currentWorkingDirectory.path}")
            elif currentCommand == "ls":
                pass
            else:
                assert False
        else:
            print(
                f"=> Detected output from previous command ({currentCommand} {currentCommandOption})"
            )
            if currentCommand == "cd":
                assert False, "Should have no output"
            elif currentCommand == "ls":
                matchOutput = re.match(r"^(\S+)\s+(\S+)", line)
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
    print("{:>20}: {:>10}".format("targetDeletionSize", targetDeletionSize))

    # Part 1
    sum = root.sumUnderLimit(limit)
    print(f"Part 1: sum of folders under {limit} is {sum}")
    assert solutionPart1 is None or solutionPart1 == sum

    # Part 2
    smallestToDelete = root.findDelete(targetSize=targetDeletionSize)
    print(f"Part 2: size of smallest folder we can delete is {smallestToDelete}")
    assert solutionPart2 is None or solutionPart2 == smallestToDelete


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day7-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solutionPart1=95437, solutionPart2=24933642)

with open("day7-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solutionPart1=1886043, solutionPart2=3842121)
