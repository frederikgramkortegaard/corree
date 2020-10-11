""" Easily define and parse command line arguments using dictionaries and types """

import re
import sys
from typing import *
from collections import defaultdict


def _lex(text: Union[str, List[str]]) -> Iterable[str]:
    """Returns a whitespace-delimited list of strings
    from the given text argument
    """
    if type(text) == list:
        text = " ".join(text)

    toks = [tok for tok in re.findall("(\[.*\]|\S*)", text) if tok != ""]

    return toks


def parse_args(
    text: str, args: Dict[str, Union[bool, List[Any]]], silent: bool = True
) -> Dict[str, Any]:
    """Identifies arguments, converts them to the expected types
    and combines them in a dictionary with their flag as the key
    """

    new_args: Dict[str, Union[bool, List[Any]]] = defaultdict(list)
    tokens: List[str] = _lex(text)
    success: bool = True
    inf_args: bool = False
    curser: int = 0

    while curser < len(tokens):

        # Find a flag
        token = tokens[curser]
        # Handle help request
        if token == "-help" or token == "--help":
            if not silent:
                print(f"Expected or Valid Arguments:")
                print("\n".join([f" >> {key}: {value}" for key, value in args.items()]))
            success = False
            break

        # We expect a flag as token, ensure that this is the case
        if token[0:2] == "--":
            offset = 2
        elif token[0] == "-":
            offset = 1
        else:
            if not silent:
                print(
                    f"token number [{curser}] with value '{token}' - is not expected as an argument, nor is it defined as a flag"
                )
            success = False
            break

        # If flag is not valid, exit.
        if token[offset:] not in args:
            if not silent:
                print(f"flag '{token}' is not a valid option, see  --help")
            success = False
            break

        # If flag is a bool, don't look for arguments
        if args[token[offset:]] == bool:
            if not silent:
                print(f"flag '{token}' is a bool, don't look for arguments")
            new_args[token[offset:]] = True
            curser += 1

        num_of_args: int = -1

        # Flag only takes a single argument
        if type(args[token[offset:]]) != list:
            print("Looking for single arg")
            num_of_args = 1

            # Set the expected argument type
            argument = args[token[offset:]]

        # Flag takes more than a single arg
        elif type(args[token[offset:]]) == list:
            num_of_args = len(args[token[offset:]])

        # Ensure enough arguments are supplied
        if num_of_args + curser >= len(tokens):
            if not silent:
                print(f"Not enough arguments given to flag '{token}'")
            success = False
            break

        # Flag takes any number of args
        if type(args[token[offset:]]) == list and num_of_args == 1:
            inf_args = True
            print(f"Setting flag '{token}' to take infinite arguments")

            # Set the expected argument type
            argument = args[token[offset:]][0]

        # Find argument(s) for flag
        idx: int = 0
        while (idx < num_of_args or inf_args) and curser < len(tokens) - 1:
            curser += 1

            # Find current arguments expected type
            # If more than one was specified
            if not inf_args and num_of_args > 1:
                argument = args[token[offset:]][idx]

            # Expected argument, got flag
            if tokens[curser].startswith("-"):
                if inf_args:
                    curser -= 1
                    break

                if not silent:
                    print(
                        f"Not enough arguments supplied to flag '{token}', flag '{tokens[curser]}' followed"
                    )
                success = False
                break

            # Assert that argument has expected type
            try:

                cast_arg = argument(tokens[curser])
                new_args[token[offset:]].append(cast_arg)

                if not silent:
                    print(
                        f"Arguments for flag '{token[offset:]}' are now {new_args[token[offset:]]}"
                    )

            except ValueError as e:
                if not silent:
                    print(
                        f"Wrong argument type for argument with value '{tokens[curser]}', expected type of '{argument}' but got type '{type(tokens[curser])}'"
                    )
                success = False
                break

            idx += 1
        curser += 1

    return success, new_args


if __name__ == "__main__":

    # Setup testing arguments
    test_args = {"run-test": bool, "silent": bool}
    success, args = parse_args(sys.argv[1:], test_args, silent=False)

    # Run test cases
    if success and args["run-test"] == True:
        test_silent = args["silent"]

        print("Entering Test Mode:\n ")

        try:
            from tests import cases

            for enum, case in enumerate(cases):
                success, args = parse_args(case[1], case[0], silent=test_silent)
                print(
                    f"Case [{enum}]: {'Failed' if success != case[2] else 'Sucessful'}"
                )
        except ImportError:
            print(" >> Could not import ./tests.py")
