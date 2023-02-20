---
sidebar_label: "✅📘 Day 2: Rock Paper Scissors"
toc_max_heading_level: 5
---

# Rock Paper Scissors

<CalloutSolution day="2"/>
<CalloutWriteup/>

## The Puzzle: Part 1

The [full puzzle text](https://adventofcode.com/2022/day/2) is available,
however I will also be pulling out key pieces of information.

> Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.
>
> The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.
>
> The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Ok, so it sounds like we just need to simulate some games of rock-paper-scissors -- not too bad!
Lets take a look at what the puzzle input is:

```cpp title="Example Puzzle Input (day2-input-test.txt)"
// Annotations added as part of the puzzle solution
// Move 1: myMove=Rock; theirMove=Paper -> Lose
// Score would be calculated as Lose (0) + Rock (1) = 1
A Y
// Move 2: myMove=Paper; theirMove=Rock -> Win
// Score would be calculated as Win (6) + Paper (2) = 8
B X
// Move 3: myMove=Scissors; theirMove=Scissors -> Tie
// Score would be calculated as Tie (3) + Scissors (3) = 6
C Z
```

This doesn't seem _too_ tough so far.
Given `myMove` and `theirMove` decoded from the input file,
we just need to calculate the `score`.
For the example above, the solution would be calculated as
`1 + 8 + 6 = 15`.

### Solution: Part 1

#### Decoding Puzzle Input

Decoding puzzle input is straightforward and
can be accomplished using the simple table below:

| `theirMove` | `myMove` | `Decode` |
| ----------- | -------- | -------- |
| `A`         | `X`      | Rock     |
| `B`         | `Y`      | Paper    |
| `C`         | `Z`      | Scissors |

To address this in code, we'll create a simple `Enum` class
to represent our moves.

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-MoveType-->
```py
class MoveType(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

We've chosen an `IntEnum` and carefully chosen its values
so that:

- We can easily decode the moves described in our puzzle input
  to a `MoveType` object.
- We can easily score a move.

To convert from the input values such as `A` or `X` to
their `MoveType` equivalent such as `MoveType.ROCK`,
we convert the input characters to their ordinal
values via [`ord(...)`] and then calculate their 'distance' from the base.

For example, `B` has a distance of `1` from `A`
and `C` has a distance of `2` from `B`.

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-MoveTypeDecode-->
```py
    @classmethod
    def from_str(cls, rawMove) -> MoveType:
        # We convert these input characters to their ordinal
        # values and then calculate their 'distance' from the base
        # For example, 'B' has a distance of 1 from 'A'
        # and 'C' has a distance of 2 from 'B'
        if rawMove in "ABC":
            dist = ord(rawMove) - ord("A") + 1
        elif rawMove in "XYZ":
            dist = ord(rawMove) - ord("X") + 1
        else:
            assert False, f"Received an unexpected move: {rawMove}"
        # This will throw a `ValueError`
        # if `dist` doesn't map to one of the enum values
        return MoveType(dist)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

#### Scoring

Game conclusion (e.g., win, tie, loss) is straightforward
and can be derived using a simple set of `if` statements
based on the [rules of rock-paper-scissors](https://en.wikipedia.org/wiki/Rock_paper_scissors).

Each game conclusion results in a specific set of points (6 for win, 3 for tie, 0 for loss)
then 1, 2 or 3 points are added based on the shape selected (1 for rock, 2 for paper, 3 for scissors).
You will notice that we chose the `MoveType` values above to align with these point values.

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-scoring-->
```py
    def scoreAgainst(self, oMove: MoveType) -> int:
        # Check for win condition
        if (
            # Formatting disabled to align `if` statement
            # fmt: off
               self == MoveType.ROCK     and oMove == MoveType.SCISSORS
            or self == MoveType.PAPER    and oMove == MoveType.ROCK
            or self == MoveType.SCISSORS and oMove == MoveType.PAPER
            # fmt: on
        ):
            print(f"{self} vs {oMove} -> Win")
            return 6 + int(self)
        # Check for tie condition
        elif int(self) == int(oMove):
            print(f"{self} vs {oMove} -> Tie")
            return 3 + int(self)
        # Else must be lose condition
        else:
            print(f"{self} vs {oMove} -> Lose")
            return 0 + int(self)
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

Then, we just need to put it all together!

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-solvePart1-->
```py
def solvePart1(lines, solution: int) -> None:
    score = 0
    for line in lines:
        # Get the moves from the puzzle input
        theirMove, ourMove = [
            MoveType.from_str(move) for move in line.split()
        ]
        # Calculate the score
        score += ourMove.scoreAgainst(theirMove)
    print(f"Calculated:  {score:}")
    if solution:
        print(f"=> Expected: {solution}")
    assert solution is None or score == solution
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

## Part 2

The [full puzzle text](https://adventofcode.com/2022/day/2) is available,
however I will also be pulling out key pieces of information.

> The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"
>
> The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated.

Oh no, the input data should be interpreted as `opponent move` + `desired win condition`,
not `opponent move` + `our move`!

On the plus side, we already have a lot of the logic needed to accomplish this 👍,
we're just missing a function to calculate `our move` from `opponent move` + `desired win condition`.
Lets call it `deriveMove(...)`!

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-deriveMove-->
```py
    def deriveMove(self, desiredOutcome: str) -> MoveType:
        if desiredOutcome == "Y":
            # Tie
            return self
        elif desiredOutcome == "Z":
            # Win
            if self == MoveType.ROCK:
                return MoveType.PAPER
            if self == MoveType.PAPER:
                return MoveType.SCISSORS
            if self == MoveType.SCISSORS:
                return MoveType.ROCK
        elif desiredOutcome == "X":
            # Lose
            if self == MoveType.ROCK:
                return MoveType.SCISSORS
            if self == MoveType.PAPER:
                return MoveType.ROCK
            if self == MoveType.SCISSORS:
                return MoveType.PAPER
        assert False, (
            f"Unknown error for opponent move of {self} and desired"
            f" outcome of {desiredOutcome}"
        )
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

All that's left is to put it together!

<!-- prettier-ignore-start -->
<!--SNIPSTART day2-solvePart2-->
```py
def solvePart2(lines, solution: int) -> None:
    score = 0
    for line in lines:
        theirMoveStr, desiredOutcome = line.split()
        theirMove = MoveType.from_str(theirMoveStr)
        ourMove = theirMove.deriveMove(desiredOutcome)
        score += ourMove.scoreAgainst(theirMove)
    print(f"Calculated:  {score}")
    if solution:
        print(f"=> Expected: {solution}")
    assert solution is None or score == solution
```
<!--SNIPEND-->
<!-- prettier-ignore-end -->

<!-- Links -->

[`ord(...)`]: https://docs.python.org/3.10/library/functions.html#ord
