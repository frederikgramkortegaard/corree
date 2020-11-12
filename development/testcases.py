""" """


from typing import *
from dataclasses import dataclass, field

@dataclass
class Case:
    input: str
    definitions: Dict[str, Any]


cases: List[Case] = list()

# -- TEST CASES -- #

cases.append(
    Case(
        input = "-name frederik",
        definitions = {
            "name": (str)
        }
    )
)


