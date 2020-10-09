""" Easily define and parse command line arguments using dictionaries and types """


import sys
from typing import *
from collections import defaultdict


def _lex(text: str) -> Iterable[str]:
    """Returns a whitespace-delimited list of strings
    from the given text argument
    """

    tokens = text.split(" ") if text.__contains__(" ") else text
    return list(filter(lambda x: x != "", tokens))


def parse_args(
    text: str, args: Dict[str, Union[bool, List[Any]]], silent: bool = True
) -> Dict[str, Any]:
    """Identifies arguments, converts them to the expected types
    and combines them in a dictionary with their flag as the key
    """

    new_args: Dict[str, Union[bool, List[Any]]] = defaultdict(list)
    tokens: List[str] = _lex(text)
    success: bool = True
    curser: int = 0

    while curser < len(tokens):

        # Find a flag
        token = tokens[curser]

        # Handle help request
        if token == "-help" or token == "--help":
            print(f"Expected or Valid Arguments:")
            print("\n".join([f" >> {key}: {value}" for key, value in args.items()]))
            success = False
            break

        # We expect a flag as token, assert that this is the case
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
                print(f"flag '{token}' is not a valid option")
            success = False
            break

        # If flag is a bool, don't look for arguments
        if args[token[offset:]] == bool:
            new_args[token[offset:]] = True
            curser += 1
            continue

        # Ensure enough arguments are supplied
        if curser + len(args[token[offset:]]) >= len(tokens):
            if not silent:
                print(f"Not enough arguments given to flag {token}")
            success = False
            break

        # Find arguments for flag
        for enum, argument in enumerate(args[token[offset:]]):
            curser += 1

            # Expected argument, got flag
            if tokens[curser].startswith("-"):
                if not silent:
                    print(
                        f"Not enough arguments supplied to flag {token}, flag {tokens[curser]} followed"
                    )
                success = False
                break

            # Assert that argument has expected type
            try:
                new_args[token[offset:]].append(argument(tokens[curser]))
            except ValueError as e:
                if not silent:
                    print(
                        f"Wrong argument type for argument [{enum}], expected type of {argument} but got type {type(tokens[curser])}"
                    )
                success = False
                break

            # Unpack single arguments encapsulated in a list
            if len(args[token[offset:]]) == 1:
                new_args[token[offset:]] = new_args[token[offset:]][0]

        curser += 1

    return success, new_args


if __name__ == "__main__":

    # Setup testing arguments
    test_args = {"run-test": bool, "silent": bool}
    success, args = parse_args(sys.argv[1:], test_args)

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
