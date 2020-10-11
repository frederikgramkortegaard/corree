""" """

from dataclasses import dataclass, field
from typing import Any


@dataclass
class case:
    inp: str
    args: dict
    output: Any
    success: bool


cases: list = list()

case_1 = case(
    inp="-words foo bar monty python",
    args={"words": [str]},
    output={"words": ["foo", "bar", "monty", "python"]},
    success=True,
)
cases.append(case_1)

case_2 = case(
    inp="-name jack",
    args={"name": str},
    output={"name": "jack"},
    success=True,
)
cases.append(case_2)

case_2 = case(
    inp="-ages 1 2 3 4 5",
    args={"ages": [int]},
    output={"ages": [1, 2, 3, 4, 5]},
    success=True,
)
cases.append(case_2)

case_2 = case(
    inp="-ages 1",
    args={"ages": [int]},
    output={"ages": [1]},
    success=True,
)
cases.append(case_2)