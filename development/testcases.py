""" """


from typing import *
from dataclasses import dataclass, field

@dataclass
class Case:
    input: str
    definitions: Dict[str, Any]
    success: bool
    output: Dict[str, Any]
    name: str = field(default=None)

cases: List[Case] = list()

# -- TEST CASES -- #

cases.extend([
    Case(
        input = "-name frederik",
        success = True,
        definitions = {
            "name": str
        },
        output = {"name": "frederik"}
    ),

    Case(
        input = "-name frederik",
        success = True,
        definitions = {
            "name": (str)
        },
        output = {"name": "frederik"}
    ),
    Case(
        input = "-name ",
        success = False,
        definitions = {
            "name": str
        },
        output = dict()
    )
])


