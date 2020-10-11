""" """

from dataclasses import dataclass, field
from typing import Any


@dataclass
class case:
    inp: str
    args: dict
    output: Any
    success: bool
    name: str = field(default=None)


cases: list = list()

cases.append(
    case(
        name="Test Infinite Words",
        inp="-words foo bar monty python",
        args={"words": [str]},
        output={"words": ["foo", "bar", "monty", "python"]},
        success=True,
    )
)

cases.append(
    case(
        inp="-name jack",
        args={"name": str},
        output={"name": "jack"},
        success=True,
    )
)

cases.append(
    case(
        inp="-ages 1 2 3 4 5",
        args={"ages": [int]},
        output={"ages": [1, 2, 3, 4, 5]},
        success=True,
    )
)

cases.append(
    case(
        inp="-ages 1",
        args={"ages": [int]},
        output={"ages": [1]},
        success=True,
    )
)