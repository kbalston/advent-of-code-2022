---
sidebar_label: "✅ Day 1: Calorie Counting"
toc_max_heading_level: 5
---

# Day 1: Calorie Counting

## The Puzzle

The [full puzzle text](https://adventofcode.com/2022/day/1) is available,
however I will also be pulling out key pieces of information.

> The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory (if any) by a blank line.

The input data today is quite straightforward.
The food being carried by each elf is listed line-by-line,
with an empty line indicating the end of the list of food items
carried by that elf.

<details>
  <summary>View snippet of input data</summary>
  <div>

```cpp
// Annotations added as part of the puzzle solution
// Elf 1: 3 food items, totalling 10292 calories
6758
5199
10292

// Elf 2: 1 food item, totalling 62522 calories
62522

// Elf 3: 2 food items, totalling 29720 calories
22990
6730
```

  </div>
</details>

As can be seen from the snippet of input data above,
each elf will be carrying one or more items of food represented by
the number of calories that food contains.

### Part 1

> In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many Calories are being carried by the Elf carrying the most Calories.
>
> Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

Advent of Code this year is starting quite simple 😄.
Each elf is carrying a number of items of food, which can be summed to count how
many calories that elf is carrying.

To solve, we simply need to iterate through all of the lines, summing the calories
seen for each line into `thisElf`. Once an elf's list of food items is terminated with
an empty line, we record the maximum value of calories seen so far into
`maxElf` and then reset `thisElf` back to zero.

```python
for line in lines:
    if not line:
        print(f"This elf was seen carrying {thisElf:6} calories")
        maxElf = max(maxElf, thisElf)
        print(f"The elf seen carrying the most calories so far was carrying {maxElf:6} calories")
        thisElf = 0
        print()
        continue
    c = int(line)
    thisElf += c
    print(f"This elf is carrying an item of food of {c:5} calories, for a total of {thisElf:6} calories so far")

print(f"The elf seen carrying the most calories was carrying {maxElf:6} calories")
```

One challenge with the solution above is that the last elf will not be fully analyzed
because that elf does not have an empty line to terminate their list of food items.
There are many ways we could consider handling this edge case.
As an example, one way to address this might be to consider recalculating the
`maxElf` value after processing every line.
Instead, for simplicity I choose to simply chose to "reconcile" the input data by ensuring that the data
ended with a newline.

```python
# Lets make sure we terminate the sequence
# with an empty line so we close out that elf's calories
if lines[-1]:
    lines.append("")
```

For the full solution, please see
[`day1-part1.py` on GitHub](https://github.com/kbalston/advent-of-code-2022/blob/main/day1/day1-part1.py).

### Part 2

#### Simple Solution

> By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.
>
> To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.
>
> Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?

Part 2 is an evolution of Part 1.
A similar core loop can be used, however we need to keep track of the top three elves rather than the top elf in Part 1.

:::info Design Decision

At this point, we are faced with a choice.
It would be more memory-efficient to only keep track of the top three elves,
however it would also require more bookkeeping.
Can we get away with a simple, naive solution?

Lets take a look at the input data to help us make this decision.

```shell
# Lets check the number of lines
$ wc --lines day1-input.txt
2255 day1-input.txt

# And the (approximate) number of elves
# '^$' is the regex pattern for an empty line
$ grep '^$' day1-input.txt | wc --lines
255
```

From the trace above 👆, we can see that there are only `2255` food items that are part of our input
and around `255` elves.
To me, this indicates that our problem set is small enough that even the most naive solution would be tractable on modern machines.

:::

Given our problem set is reasonable small, lets start with a simple implementation that builds
an unsorted list that contains the number of calories that each elf is carrying.

We can store our calorie count for each elf in a list, `allElves`.

```python
allElves = []
```

And then just append each elf's calorie count, `thisElf`, to `allElves`.

```python
for line in lines:
    if not line:
        print("Empty line detected -> end of this elf's food")
        allElves += [thisElf]
        thisElf = 0
        continue
    c = int(line)
    thisElf += c
```

Now, we simply need to sort the list and keep the top three entries.

```python
topThree = sum(sorted(allElves, reverse=True)[0:3])
print(f"The top three elves are carrying a sum of {topThree:6} calories")
```

For the full solution, please see
[`day1-part2.py` on GitHub](https://github.com/kbalston/advent-of-code-2022/blob/main/day1/day1-part2.py).

#### More Complex Solution

But we can do better!
Perhaps we could use a module like
[`bisect`](https://docs.python.org/3/library/bisect.html)
to keep the list sorted as we go?
Unfortunately, insertions are `O(n)` 🤔.

Better yet, perhaps we could use the
[`heapq`](https://docs.python.org/3/library/heapq.html)
module!
This module implements a priority queue, so insertions should only be `O(log n)`,
which seems well-suited for our purpose.
Lets rewrite our solution such that we only keep track of the top three elves using
[`heapq`](https://docs.python.org/3/library/heapq.html).

We'll start by initializing `allElves` to `[-1, -1, -1]`.
We do this so `allElves` is already the correct sized and we can just pop off the `-1` values
as we learn how much each elf is carrying.

```python
# Initialize variables used for summation
numberOfElvesToTrack = 3
# We'll start with a value of `-1` since
# that should be smaller than any value any elf can carry
allElves = [-1] * numberOfElvesToTrack
```

Then, we iterate through `lines` in a similar way to the previous solution,
except we call `heappushpop(...)` to insert `thisElf` and pop the smallest value.

```python
for line in lines:
    if not line:
        print(f"This elf was seen carrying {thisElf:6} calories")
        # We assume that `-1` is smaller than any
        # possible calorie amount
        assert(thisElf > 0)
        # `heappushpop` will add `thisElf` to `allElves` and pop the smallest value
        heapq.heappushpop(allElves, thisElf)
        thisElf = 0
        continue
    c = int(line)
    thisElf += c
```

For the full solution, please see
[`day1-part2b.py` on GitHub](https://github.com/kbalston/advent-of-code-2022/blob/main/day1/day1-part2b.py).
