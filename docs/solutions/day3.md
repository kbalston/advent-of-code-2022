---
sidebar_label: "✅ Day 3: Rucksack Reorganization"
toc_max_heading_level: 5
---

# Rucksack Reorganization

## Part 1

### Puzzle

The [full puzzle text](https://adventofcode.com/2022/day/3) is available,
however I will also be pulling out key pieces of information.

> Each rucksack has two large compartments. All items of a given type are meant to go into exactly one of the two compartments. The Elf that did the packing failed to follow this rule for exactly one item type per rucksack.
>
> The Elves have made a list of all of the items currently in each rucksack (your puzzle input), but they need your help finding the errors. Every item type is identified by a single lowercase or uppercase letter (that is, a and A refer to different types of items).
>
> The list of items for each rucksack is given as characters all on a single line. A given rucksack always has the same number of items in each of its two compartments, so the first half of the characters represent items in the first compartment, while the second half of the characters represent items in the second compartment.

```cpp title="Example Puzzle Input (day3-input-test.txt)"
// Annotations added as part of the puzzle solution
// First rucksack is divided in two
vJrwpWtwJgWrhcsFMMfFFhFp
// First compartment:
//   vJrwpWtwJgWr
// Second compartment:
//   hcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
```

This seems reasonably straightforward again!
We just just need to divide each line into two halves,
then iterate through each compartment
and find the single letter that is present in each.

From the example puzzle input above,
we can see that lines are of variable size.

### Solution

The "nuts and bolts" of the solution is straightforward,
we need to divide each line into two compartments and then
pass a string representing each compartment to the `getScore` function.

<!-- prettier-ignore-start -->
<!--SNIPSTART day3-part1-->
```py
def solvePart1(lines: list[str], expected: int) -> None:
    calculated = 0
    spacer = "=" * 10
    for i, line in enumerate(lines, start=1):
        print(f"{spacer} Part 1: Rucksack {i} {spacer}")
        halfway = int(len(line) / 2)
        # Divide into two compartments
        firstCompartment = line[0:halfway]
        secondCompartment = line[halfway:]
        print(firstCompartment)
        print(secondCompartment)
        # Find the first shared letter in the compartments
        calculated += getScorePart1(
            firstCompartment, secondCompartment
        )
    checkSolution(calculated=calculated, expected=expected)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

In the `getScore` function, we use the
[`ord` function](https://docs.python.org/3/library/functions.html#ord)
to get the integer representation of each character and compare that
against `ord("a")` or `ord("A")`, as appropriate.
We do this because `a` through `z` are assigned scores of 1 through 26
and `A` through `Z` are assigned scores of 27 through 52.

Note: this `getScore` function is a bit more complicated than it needs
to be because it supports both part 1 and part 2
(where you also need to compare against a third rucksack, `ruckC`).

<!-- prettier-ignore-start -->
<!--SNIPSTART day3-getScore-->
```py
def getScore(
    ruckA: str, ruckB: str, ruckC: Optional[str] = None
) -> int:
    """Return the score as an integer of a given elf's rucksack
    or rucksack compartment by finding the first letter
    that is present in all provided rucksacks.

    Will assert if no letters are found in common.
    """
    for letter in ruckA:
        if letter in ruckB and (ruckC is None or letter in ruckC):
            print(f"=> found '{letter}' in all")
            if letter.islower():
                return ord(letter) - ord("a") + 1
            else:
                return ord(letter) - ord("A") + 27
    assert False, "Unable to find a common letter"
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

## Part 2

### Puzzle

> As you finish identifying the misplaced items, the Elves come to you with another issue.
>
> For safety, the Elves are divided into groups of three. Every Elf carries a badge that identifies their group. For efficiency, within each group of three Elves, the badge is the only item type carried by all three Elves. That is, if a group's badge is item type B, then all three Elves will have item type B somewhere in their rucksack, and at most two of the Elves will be carrying any other item type.
>
> The problem is that someone forgot to put this year's updated authenticity sticker on the badges. All of the badges need to be pulled out of the rucksacks so the new authenticity stickers can be attached.
>
> Additionally, nobody wrote down which item type corresponds to each group's badges. The only way to tell which item type is the right one is by finding the one item type that is common between all three Elves in each group.

Part 2 seems like a simple evolution on part 1.
Instead of treating each line as a rucksack with two compartments,
we treat every three lines as separate rucksucks (each with a single compartment).

In practical terms, we just need to compare three lists against one-another
rather than two.

### Solution

To start, we've leveraged the BSD-licensed `grouper` function from the
[`itertools` recipes](https://docs.python.org/3/library/itertools.html#itertools-recipes).
It allows us to iterate on `n` items from an iterable at a time,
rather than just one.

<!-- prettier-ignore-start -->
<!--SNIPSTART day3-grouper-->
```py
# From https://docs.python.org/3/library/itertools.html
# License: Zero Clause BSD License
def grouper(iterable, n, *, incomplete="fill", fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == "fill":
        return zip_longest(*args, fillvalue=fillvalue)
    if incomplete == "strict":
        return zip(*args, strict=True)
    if incomplete == "ignore":
        return zip(*args)
    else:
        raise ValueError("Expected fill, strict, or ignore")
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

Once we have the `grouper` function in place,
part 2 is similar to part 1:

<!-- prettier-ignore-start -->
<!--SNIPSTART day3-part2-->
```py
def solvePart2(lines: list[str], expected: int) -> None:
    calculated = 0
    spacer = "=" * 10
    # Group in strict mode so if an iteration has fewer than
    # `n` items, `grouper` asserts
    iterator = grouper(iterable=lines, n=3, incomplete="strict")
    for i, elves in enumerate(iterator, start=1):
        print(f"{spacer} Part 2: Rucksack {i} {spacer}")
        for elf in elves:
            print(elf)
        # Find the first shared letter in the compartments
        calculated += getScorePart2(*elves)
    checkSolution(calculated=calculated, expected=expected)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

And in fact, a simple extension on `getScorePart1` can be made to support
both part1 and part 2 🎉.

<!-- prettier-ignore-start -->
<!--SNIPSTART day3-getScorePart2-->
```py
def getScorePart2(
    ruckA: str, ruckB: str, ruckC: Optional[str] = None
) -> int:
    """Return the score as an integer of a given elf's rucksack
    or rucksack compartment by finding the first letter
    that is present in all provided rucksacks.

    Will assert if no letters are found in common.

    Supports both part 1 and part 2.
    """
    for letter in ruckA:
        if letter in ruckB and (ruckC is None or letter in ruckC):
            print(f"=> found '{letter}' in all")
            if letter.islower():
                return ord(letter) - ord("a") + 1
            else:
                return ord(letter) - ord("A") + 27
    assert False, "Unable to find a common letter"
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->
