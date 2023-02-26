#!/usr/bin/env python3

# type: ignore

# mypy typing is a bit of a pain in this solution
# because of how we've reconciled Node types to plain floats
# as their values become known

# TODO: Rethink this approach, likely splitting out the Node and float
# types so that statically checking types is more straightforward

from __future__ import annotations
import operator

import os
import re
import logging

logging.basicConfig(format="%(message)s", level=logging.INFO)


def operatorConst(left, right):
    assert right is None
    assert isinstance(left, int)
    return left


def operatorEqual(left, right):
    # This function should never be invoked
    assert False


def operatorSymbol(left, right):
    # This function should never be invoked
    assert False


def operatorSubRight(left, right):
    return right - left


class Node:
    def __init__(self, name, op, left, right=None):
        self.name = name
        self.setOp(op)
        self.left = left
        self.right = right

    def __repr__(self):
        if self.op == operatorSymbol:
            return "humn"
        elif self.op == operatorConst:
            return str(self.left)
        else:
            right = f" {self.right}" if self.right else ""
            return f"({self.left} {self.op.__name__}{right})"

    def setOp(self, op):
        opInvLeft = None
        opInvRight = None
        if isinstance(op, str):
            match op:
                case "+":
                    op = operator.add
                    opInvLeft = operator.sub
                case "-":
                    op = operator.sub
                    opInvLeft = operator.add
                    opInvRight = operatorSubRight
                case "*":
                    op = operator.mul
                    opInvLeft = operator.truediv
                case "/":
                    op = operator.truediv
                    opInvLeft = operator.mul
                case "=":
                    op = operatorEqual
                case unknown:
                    assert False, f"Unknown operator: {unknown}"
        self.op = op
        self.opInvLeft = opInvLeft
        if opInvRight is None:
            self.opInvRight = opInvLeft
        else:
            self.opInvRight = opInvRight

    def isConstant(self):
        return self.op == operatorConst

    def isSymbolic(self):
        return self.op == operatorSymbol

    def readyToInvert(self):
        if self.isConstant():
            return False
        if self.op == operatorSymbol:
            return False
        return self.left.isConstant() or self.right.isConstant()

    def readyToOperate(self):
        if self.isConstant():
            return False
        if self.isSymbolic():
            return False
        return (
            self.left.isConstant()
            and self.right is not None
            and self.right.isConstant()
        )

    def _operate(self, otherSide):
        if isinstance(self.left, Node):
            if otherSide is None:
                self.left._operate(self.right)
            else:
                self.left._operate(otherSide)
        if isinstance(self.right, Node):
            if otherSide is None:
                self.right._operate(self.left)
            else:
                self.right._operate(otherSide)
        if self.readyToOperate():
            self.left = self.op(self.left.left, self.right.left)
            self.op = operatorConst
            self.right = None

    def invertIfPossible(self, otherSide):
        readyToInvert = self.readyToInvert()
        if (
            readyToInvert
            and otherSide is not None
            and otherSide.isConstant()
        ):
            assert self.opInvLeft
            assert self.opInvRight
            if self.right.isConstant():
                assert otherSide.isConstant()
                otherSide.left = self.opInvLeft(
                    otherSide.left, self.right.left
                )
                return self.left
            elif self.left.isConstant():
                assert otherSide.isConstant()
                otherSide.left = self.opInvRight(
                    otherSide.left, self.left.left
                )
                return self.right
            else:
                assert False
        else:
            return self

    def operate(self):
        # Part 1
        if self.op != operatorEqual:
            self._operate(otherSide=None)
        # Part 2
        else:
            self._operate(otherSide=None)
            self.left = self.left.invertIfPossible(
                otherSide=self.right
            )
            self.right = self.right.invertIfPossible(
                otherSide=self.left
            )

    def _substitute(self, s, nodes):
        assert s in nodes
        newNode = nodes[s]
        return newNode

    def substitute(self, nodes):
        if isinstance(self.left, str):
            logging.debug(f"Substituting left node of '{self.left}'")
            self.left = self._substitute(self.left, nodes)
            logging.debug(f"=> Received '{self.left}'")
            if isinstance(self.left, Node):
                self.left.substitute(nodes)
        if isinstance(self.right, str):
            logging.debug(
                f"Substituting right node of '{self.right}'"
            )
            self.right = self._substitute(self.right, nodes)
            logging.debug(f"=> Received '{self.right}'")
            if isinstance(self.right, Node):
                self.right.substitute(nodes)


def solve(lines, part1, solution) -> None:
    pattern = re.compile(r"(\S+): (.*)")
    nodes = dict()
    for _, line in enumerate(lines):
        m = pattern.match(line)
        name = m.group(1)
        value = m.group(2).split()
        if part1 is False:
            if name == "root":
                value[1] = "="
            if name == "humn":
                value = (None, operatorSymbol, None)
        if len(value) == 1:
            value = (int(value[0]),)
            node = Node(name, operatorConst, value[0])
        else:
            node = Node(name, value[1], value[0], value[2])
        nodes[node.name] = node
        logging.debug(node)

    if part1:
        root = nodes["root"]
        root.substitute(nodes)
        root.operate()
        assert root.op == operatorConst
        calculated = int(root.left)
    else:
        root = nodes["root"]
        logging.debug("-" * 10)
        root.substitute(nodes)
        logging.debug("-" * 10)
        for _ in range(500):
            root.operate()
            logging.debug("-" * 10)
        root.operate()
        assert root.op == operatorEqual
        if root.left.name == "humn":
            calculated = int(root.right.left)
        else:
            calculated = int(root.left.left)

    logging.info(f"Calculated is {calculated}")
    logging.info(f"=> Expecting  {solution}")
    assert calculated == solution


os.chdir(os.path.realpath(os.path.dirname(__file__)))

# Part 1
with open("day21-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    solution=152,
)

with open("day21-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=True,
    solution=155708040358220,
)


# Part 2
with open("day21-input-test.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    solution=301,
)

with open("day21-input.txt", "r", encoding="utf-8") as inputFile:
    lines = inputFile.read().splitlines()
solve(
    lines,
    part1=False,
    solution=3342154812537,
)
