""" Test-Cases to be used in rapidy.py when run with flag '--run-tests' """

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
        name="Test Infinite Strings",
        inp="-words foo bar monty python",
        args={"words": [str]},
        output={"words": ["foo", "bar", "monty", "python"]},
        success=True,
    )
)

cases.append(
    case(
        name="Test Single String",
        inp="-name jack",
        args={"name": str},
        output={"name": "jack"},
        success=True,
    )
)

cases.append(
    case(
        name="Test Infinite Integers",
        inp="-ages 1 2 3 4 5",
        args={"ages": [int]},
        output={"ages": [1, 2, 3, 4, 5]},
        success=True,
    )
)

cases.append(
    case(
        name="Test Infinite Integers with 1 argument given",
        inp="-ages 1",
        args={"ages": [int]},
        output={"ages": [1]},
        success=True,
    )
)

cases.append(
    case(
        name="Test Infinite Integers with 0 arguments given",
        inp="-ages",
        args={"ages": [int]},
        output={"ages": []},
        success=True,
    )
)

cases.append(
    case(
        name="Test Multiple Expected Argument Types",
        inp="--IP-PORT 192.0.0.1 8080",
        args={"IP-PORT": [str, int]},
        output={"IP-PORT": ["192.0.0.1", 8080]},
        success=True,
    )
)

cases.append(
    case(
        name="Test Infinite Strings with 0 arguments given",
        inp="--foods",
        args={"foods": [str]},
        output={"foods": []},
        success=True,
    )
)

cases.append(
    case(
        name="Test Two Expected Arguments But One Given",
        inp="--foods pizza",
        args={"foods": [str, str]},
        output={"foods": []},
        success=False,
    )
)