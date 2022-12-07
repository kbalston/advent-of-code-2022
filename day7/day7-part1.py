#!/usr/bin/env python3
import os
import re
from collections import deque
from pathlib import Path


class FilesystemItem:
    def __init__(self, path) -> None:
        self.path = path
        self.size = 0
        self.totalSize = None
        # self.childrenFiles = []
        self.childrenFolders = []

    def __repr__(self) -> str:
        return f"{self.path.resolve()}#{self.size}"

    def calculateSize(self) -> int:
        self.totalSize = self.size
        for child in self.childrenFolders:
            self.totalSize += child.calculateSize()
        return self.totalSize

    def sumUnderLimit(self, limit):
        self.calculateSize()
        sum = 0
        # Add self
        if self.totalSize < limit:
            sum += self.totalSize
        # Add children recursively
        for child in self.childrenFolders:
            sum += child.sumUnderLimit(limit)
        return sum

    # def calculateSizeUnderLimit(self, limit, sumUnderLimit):
    #     self.calculateSize()
    #     for child in self.childrenFolders:
    #         sumUnderLimit += child.calculateSizeUnderLimit(limit, sumUnderLimit)
    #     if self.totalSize < limit:
    #         return
    #     return sumUnderLimit


def solve(lines, limit=100000, solution=None):
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
                    currentWorkingDirectory.childrenFolders.append(nextWorkingDirectory)
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
                matchOutput = re.match("^(\S+)\s+(\S+)", line)
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

    sum = root.sumUnderLimit(limit)

    assert solution is None or solution == sum
    print(f"Solution is '{sum}'")
    return sum


os.chdir(os.path.realpath(os.path.dirname(__file__)))

with open("day7-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=95437)
# solve(lines, solution=None)

with open("day7-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(lines, solution=None)
