---
sidebar_label: "✅📘 Day 4: Camp Cleanup"
sidebar_position: 4
toc_max_heading_level: 5
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Camp Cleanup

<CalloutSolution day="4"/>
<CalloutWriteup/>

## Part 1

### Puzzle

The [full puzzle text](https://adventofcode.com/2022/day/4) is available,
however I will also be pulling out key pieces of information.

> Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.
>
> However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

```cpp title="Example Puzzle Input (day4-input-test.txt)"
// Annotations added as part of the puzzle solution
// Pair of elf assignments:
//   Elf 1: 2,3,4
//   Elf 2:         6,7,8
// No overlap of assignments
2-4,6-8
2-3,4-5
5-7,7-9
// Pair of elf assignments:
//   Elf 1: 2,3,4,5,6,7,8
//   Elf 2:   3,4,5,6,7
// Full overlap of elf 2's assignment by elf 1
2-8,3-7
6-6,4-6
// Pair of elf assignments:
//   Elf 1: 2,3,4,5,6
//   Elf 2:     4,5,6,7,8
// Partial overlap between elf 1 and elf 2 assignments
2-6,4-8
```

This doesn't seem too hard!
That said, there's likely a number of different ways of representing the ranges of numbers 🤔.
Lets take a look at the full puzzle input to see how big these ranges get
to understand how careful we need to be about performance.

From a quick scroll through, it looks like the largest range may be something like `1-99`
— quite small!

We can confirm this with a short shell command to show the size of each assignment in the input:

<Tabs>
<TabItem value="Command">

```bash
# Split pairs of assignments into multiple lines
sed 's/,/\n/g' day4-input.txt |
# Subtract the lower bound of the assignment from
# the upper bound, to calculate the size of the assignment
awk -F '-' 'print $2 - $1 + 1}' |
# Sort lines numerically
sort -n |
# Count ranges received
uniq --count |
# Only keep the largest ranges
tail
```

</TabItem>
<TabItem value="Output">

```bash
     10 90
     18 91
     12 92
      7 93
      6 94
     14 95
     13 96
     15 97
     10 98
      6 99
```

</TabItem>

</Tabs>

Given the ranges shown above 👆 aren't any larger than ~100, even a naive list-based representation
of the range that contained every number would be reasonable.

If the ranges were quite large, we might want to consider a more efficient format that understood
ranges of numbers more naturally (e.g., instead of working with a list of all of the numbers between 1 and 99,
it might just store the lower and upper bounds).

### Solution

#### Code: `ElfPair`

To start, I created a simple `ElfPair` class to hold a pair of elf assignments.
It uses a list-of-lists to hold a given pair of elf assignments.

For example, the first assignment from the example above

```
//   Elf 1: 2,3,4
//   Elf 2:         6,7,8
```

would be stored as the following list in `ElfPair`'s `assignments` instance variable:

```py
[
    [ 2, 3 ],
    [ 6, 8 ],
]
```

The boilerplate components of `ElfPair` for managing `assignments`
are shown below.

<!-- prettier-ignore-start -->
<!--SNIPSTART day4-elfpair-->
```py
class ElfPair:
    def __init__(self) -> None:
        # A simple two-dimensional list of integers
        # Intent is that:
        # The first index corresponds with the elf
        #   e.g., self.assignments[1] corresponds with Elf B
        # The second index corresponds with
        #   the lower and upper bounds of that elf's assignment
        #   e.g., self.assignments[1][0] corresponds with
        #   Elf B's lower assignment bound
        self.assignments: List[List[int]] = []

    def __str__(self) -> str:
        return f"Elf={self.assignments}"

    def addAssignment(self, assignments: list[int]) -> None:
        self.assignments.append(assignments)

    def getAssignmentSet(self, index: int) -> set[int]:
        assert len(self.assignments) >= index
        return set(
            range(
                self.assignments[index][0],
                self.assignments[index][1] + 1,
            )
        )
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

#### Code: `hasOverlap`

With that out of the way,
we can focus on `hasOverlap`, which calculates
whether or not a given elf pair's assignments overlap.

In part 1, we're looking for a full overlap
(i.e., `requireFullOverlap=True`),
so we're just checking to see if one of the two assignments is a
[subset](https://docs.python.org/3/library/stdtypes.html#frozenset.issubset)
of the other.
As specific examples from the sample input shown above,

- `2-4,6-8` describes "no overlap" because the two ranges
  `(2,4)` and `(6,8)` are completely disjoint.
- `2-8,3-7` describes a "full overlap" satisfying part 1
  because the range `(3,7)` is completely contained within `(2,8)`.
- `2-6,4-8` only describes a "partial overlap" which does
  not satisfy part 1 because the range `(2,6)` is not completely
  contained within `(4,8)` (and vice-versa).

<!-- prettier-ignore-start -->
<!--SNIPSTART day4-hasoverlap-->
```py
    # Within ElfPair class
    def hasOverlap(self, requireFullOverlap: bool) -> bool:
        assert len(self.assignments) == 2
        elfA = self.getAssignmentSet(0)
        elfB = self.getAssignmentSet(1)

        # Part 1
        if requireFullOverlap:
            # Full overlap requires one of these
            # ranges to be a subset of the other
            return elfA.issubset(elfB) or elfB.issubset(elfA)
        # Part 2
        else:
            # Partial overlap just requires these sets to not be disjoint
            # e.g., there is at least one shared number between these two sets
            return not elfA.isdisjoint(elfB)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

#### Code: `solve`

This `solve(...)` function isn't too complicated --
it:

- Reads the data in line-by-line
- Splits on `,` and `-` to extract the relevant info
- Calls `addAssignment(...)` to ingest the info into `ElfPair`
- Iterates through all `ElfPair`s and calls `hasOverlap` on each

<!-- prettier-ignore-start -->
<!--SNIPSTART day4-solve-->
```py
def solve(
    lines: list[str], solution: int, requireFullOverlap: bool
) -> None:
    pairs = []

    # Read in data line-by-line
    for line in lines:
        # Split string on , to extract the ranges
        split = line.split(",")
        # Then split on - to get the bounds
        first = split[0].split("-")
        second = split[1].split("-")
        pair = ElfPair()
        # Ingest the upper and lower bounds into the `ElfPair`
        pair.addAssignment([int(x) for x in first])
        pair.addAssignment([int(x) for x in second])
        pairs.append(pair)

    # Iterate through elf pairs and find overlap
    score = 0
    for i, pair in enumerate(pairs, start=1):
        print(f"Checking elf pair {i:>4}: {pair}", end="")
        if pair.hasOverlap(requireFullOverlap):
            score += 1
            print(" -> has overlap")
        else:
            print(" -> does NOT have overlap")

    print(f"Solution is  {score}")
    print(f"=> Expecting {solution}\n")
    assert score == solution
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

## Part 2

### Puzzle

> It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

Great — part 2 is just a simple extension on part 1 🎉.

We just need to update our existing function which looks for full overlap between pairs of elf assignments
(i.e., one assignment is a subset of another) to look for a partial overlap instead!

### Solution

#### Code: `hasOverlap`

In part 2, we're looking for a partial overlap
(i.e., `requireFullOverlap=False`),
so we're checking to see if the two assignment ranges are
[disjoint](https://docs.python.org/3/library/stdtypes.html#frozenset.isdisjoint)
(i.e., there are no numbers in common between the two
sets of numbers).

As specific examples from the sample input shown above,

- `2-4,6-8` describes "no overlap" because the two ranges
  `(2,4)` and `(6,8)` are completely disjoint.
- `2-8,3-7` describes a "full overlap" satisfying both parts 1 and 2
  because the full range `(3,7)` can be contained within `(2,8)`.
- `2-6,4-8` describes a "partial overlap" between `(4,6)`
  which does not satisfy part 1, but does satisfy part 2.

<!-- prettier-ignore-start -->
<!--SNIPSTART day4-hasoverlap-->
```py
    # Within ElfPair class
    def hasOverlap(self, requireFullOverlap: bool) -> bool:
        assert len(self.assignments) == 2
        elfA = self.getAssignmentSet(0)
        elfB = self.getAssignmentSet(1)

        # Part 1
        if requireFullOverlap:
            # Full overlap requires one of these
            # ranges to be a subset of the other
            return elfA.issubset(elfB) or elfB.issubset(elfA)
        # Part 2
        else:
            # Partial overlap just requires these sets to not be disjoint
            # e.g., there is at least one shared number between these two sets
            return not elfA.isdisjoint(elfB)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

#### Code: `solve`

Luckily, we can use the [same `solve(...)` function from part 1](#code-solve) 🥳.
