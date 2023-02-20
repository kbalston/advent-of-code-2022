---
sidebar_label: "✅ Day 5: Supply Stacks"
toc_max_heading_level: 5
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

# Supply Stacks

:::info Full solution

The full solution for this day's puzzle can be found on
[GitHub](https://github.com/kbalston/advent-of-code-2022/tree/main/day5).

:::

## Puzzle

### Part 1

The [full puzzle text](https://adventofcode.com/2022/day/5) is available,
however I will also be pulling out key pieces of information.

> The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.
>
> The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.
>
> The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.
>
> They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input).
>
> After the rearrangement procedure completes, what crate ends up on top of each stack?

This doesn't seem too tough -- we'll likely keep track of the position of each stack of crates
in a conventional stack-like data structure (where we push and pop from the top of the stack),
then execute the rearrangement procedure to modify the crate positions using those pushes and pops.

### Example Puzzle Input

```cpp title="Example Puzzle Input (day5-input-test.txt)"
// Annotations added as part of the puzzle solution
// List of initial crate state
// Height 2: crate in column 2
    [D]
// Height 1: crates in columns 1 and 2
[N] [C]
// Height 0: crates in all columns
[Z] [M] [P]
 1   2   3

// List of crate movements
// Move 1 crate from the top of column 2 to column 1
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```

### Part 2

> Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.
>
> The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

This doesn't seem like too much of a stretch from part 1
-- we just need to change how crates are moved from
column to column.

In part 1, in a multi-crate movement command such as `move 3 from 1 to 3`,
we can move each crate individually to its final location.
The implication of this is that `move 3 from 1 to 3` is the same as executing
`move 1 from 1 to 3` three times.

In part 2, this is no longer the case because all crates are moved together
as a single unit.
On the plus side, we do not need to change the bulk of code to accommodate this extension 🎉.

## Solution

### Code: `solve`

There's three main steps to our `solve` function:

- `parseCratePositions`
- `executeCrateMoves`
- `extractSolution`

Each will be called out in more detail below 👍.

<!-- prettier-ignore-start -->
<!--SNIPSTART day5-solve-->
```py
def solve(
    lines: list[str], moveMultiple: bool, solution: str
) -> None:
    # Step 1: Parse initial state
    print("*** Parsing initial crate state ***")
    spots = parseCratePositions(lines)

    # Step 2: Execute crate movement from list
    print("\n*** Executing crate moves ***")
    executeCrateMoves(spots, lines, moveMultiple)

    # Step 3: Extract solution topmost crates in each column
    calculated = extractSolution(spots)

    print()
    print(f"Solution is {calculated}")
    print(f"Expecting   {solution}")
    assert calculated == solution
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

### Code: `parseCratePositions`

`parseCratePositions` is in charge of parsing the initial crate
positions from the puzzle input and populating our data structures.
This code could likely be a bit more clever, but it just divides
each line into three character chunks and assumes that if the chunk
is not three spaces, then the middle character will
describe a crate (e.g., `[D]`).

After we've parsed all of the crates for a given line,
these are just appended into our `spots` variable.
`spots` is a list of deques where the index of the list
corresponds with the crate column.

As a specific example, from our [puzzle input](#example-puzzle-input):

```
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3
```

will be parsed as

```py
[
    deque([]),
    deque(['N', 'Z']),
    deque(['D', 'C', 'M']),
    deque(['P'])
]
```

You'll notice that there are three columns listed above, but four entries in `spots`.
This was an intentional choice to keep the column indexes listed above a direct map
into `spots`, but it would likely be a good idea to remove this index 🙂.

<!-- prettier-ignore-start -->
<!--SNIPSTART day5-parseCratePositions-->
```py
def parseCratePositions(
    lines: list[str],
) -> list[deque[Any]]:
    spots: Optional[list[deque[Any]]] = None
    while lines:
        line = lines.pop(0)
        print(f"\nParsing line '{line}'")
        # There's likely a more elegant way of detecting
        # the transition from crate state to movement list
        # however for now it's likely fine to just look for the
        # column numbers like " 1   2   3"
        if "1" in line:
            print(
                f"=> Detected a '1' in the line"
                f" => Assuming end of crate list"
            )
            # Also pop the next line, which should be empty
            nextLine = lines.pop(0)
            assert nextLine == ""
            assert spots is not None
            return spots

        index = 0
        values = []
        # For this line we're parsing right now,
        # read three characters at a time and decode as a crate
        while True:
            crate = line[index : index + 3]
            assert crate is not None
            # Check for no crate in this spot
            if crate == "   ":
                value = None
            else:
                # Take the middle position as the crate
                value = crate[1]
            values.append(value)
            index += 4
            if index > len(line):
                # Done reading all crates at this height
                break
        print(f"=> Received {values}")
        assert values
        # Lazily allocate this since we don't know up front
        # how many columns we need
        if spots is None:
            spots = [deque() for _ in values]
            spots.append(deque())
        # Append this line's crate positions into `spots`
        for i, letter in enumerate(values):
            if letter is not None:
                print(f"==> {letter} is at index {i + 1}")
                spots[i + 1].append(letter)
    assert False
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

### Code: `executeCrateMoves`

Now that we have our `spots` data structure populated,
we can read and execute our instructions one-by-one!

For part 1, each individual movement is simple, just a
[`popleft`](https://docs.python.org/3/library/collections.html#collections.deque.popleft)
from the source location followed by an
[`appendleft`](https://docs.python.org/3/library/collections.html#collections.deque.appendleft)
to the destination location.

For part 2, we take a very similar approach, but append all crates into a temporary
`cratesToMove` deque. Once all crates have been moved there, we `appendLeft` them to
their final location in the destination column.
We could avoid this temporary copy, but it would likely add some additional complexity.

<!-- prettier-ignore-start -->
<!--SNIPSTART day5-executeCrateMoves-->
```py
def executeCrateMoves(
    spots: list[deque[str]], lines: list[str], moveMultiple: bool
) -> None:
    pattern = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in lines:
        # Parse the line into relevant variables
        print(f"\nParsing line '{line}'")
        matches = re.match(pattern, line)
        assert matches
        moves = int(matches.group(1))
        source = int(matches.group(2))
        dest = int(matches.group(3))
        assert spots is not None
        # Perform the movement
        # Part 1 - move each crate directly to the destination, one by one
        if not moveMultiple:
            for move in range(moves):
                print(f"=> Moving #{move} from {source} to {dest}")
                crate = spots[source].popleft()
                spots[dest].appendleft(crate)
        # Part 2 - move each crate to `cratesToMove` temporarily
        # before moving them to their final destination
        # Compared to part 1, when groups of crates are moved together,
        # they will not have their positions reversed
        else:
            cratesToMove: deque[str] = deque()
            for move in range(moves):
                print(f"=> Moving #{move} from {source} to {dest}")
                crate = spots[source].popleft()
                cratesToMove.appendleft(crate)
            for crate in cratesToMove:
                spots[dest].appendleft(crate)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

### Code: `extractSolution`

Finally, we have `extractSolution`.
This function is quite simple,
it just returns the concatenation of
the first crate in every position (if there is a crate in that position).

<!-- prettier-ignore-start -->
<!--SNIPSTART day5-extractSolution-->
```py
def extractSolution(spots: list[deque[str]]) -> str:
    # Returns the topmost crate if it exists,
    # otherwise it returns an empty string
    def extractFirst(crates: deque[str]) -> str:
        if len(crates) > 0:
            return crates[0]
        else:
            return ""

    # Concatenate together the topmost crate from each position
    return "".join(map(extractFirst, spots))
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->
