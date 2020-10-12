""" Easily define and parse command line arguments using dictionaries and types """

import re
import sys
import logging
from typing import *
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)


def _lex(text: Union[str, List[str]]) -> Iterable[str]:
    """Returns a whitespace-delimited list of strings
    from the given text argument
    """
    if type(text) == list:
        text = " ".join(text)

    toks: List[str] = [tok for tok in re.findall("(\[.*\]|\S*)", text) if tok != ""]

    return toks


def parse_args(text: str, args: Dict[str, Union[bool, List[Any]]]) -> Dict[str, Any]:
    """Identifies arguments, converts them to the expected types
    and combines them in a dictionary with their flag as the key
    """

    new_args: Dict[str, Any] = defaultdict(list)
    tokens: List[str] = _lex(text)
    inf_args: bool = False
    success: bool = True
    cursor: int = 0

    # Handle help requests
    if len(tokens) > 0 and (tokens[cursor] == "-help" or tokens[cursor] == "--help"):
        print(f"Expected or Valid Arguments:")
        print("\n".join([f" >> {key}: {value}" for key, value in args.items()]))
        return (True, dict())

    # Set default values
    for key, value in args.items():

        if type(value) in [list, tuple]:
            new_args[key] = type(value)()
        elif value == bool:
            new_args[key] = False
        elif value in [str, float, int]:
            new_args[key] = None
        else:
            logging.error(f"Unsupported Expected Argument Type {type(value)}, {value}")
            return (False, dict())

    # Iterate through tokens
    while cursor < len(tokens):

        token = tokens[cursor]

        # Find number of prefixed dashes
        offset: int = 0
        while token[offset:].startswith("-"):
            offset += 1

        if offset == 0:
            logging.error(
                f"Token number [{cursor}] with value '{token}' - is not expected as an argument, nor is it defined as a flag"
            )
            success = False
            break

        # Remove prefixed dashes from flag
        token = token[offset:]

        # Flag is not valid
        if token not in args:
            logging.error(f"Flag '{token}' is not a valid option, see --help")
            success = False
            break

        # Flag does not take multiple arguments
        if type(args[token]) not in [list, tuple]:

            # Flag is a bool, don't look for arguments
            if args[token] == bool:
                logging.info(f"Flag '{token}' is a bool, don't look for arguments")
                new_args[token] = True
                cursor += 1
                continue

            logging.info(f"Flag '{token}' is only Looking for a single argument")
            num_of_args = 1

            # Set the expected argument type
            argument = args[token]

        # Flag takes more than a single arg
        else:
            num_of_args = len(args[token])

            # Flag takes any number of args
            if num_of_args == 1:
                inf_args = True
                logging.info(
                    f"Flag '{token}' takes infinite arguments of type {args[token][0]}"
                )
                argument = args[token][0]
            else:
                logging.info(f"Flag '{token}' takes {num_of_args} arguments")

        # Ensure enough arguments are supplied
        if num_of_args + cursor >= len(tokens) and not inf_args:
            logging.error(f"Not enough arguments given to flag '{token}'")
            success = False
            break

        # Find argument(s) for flag
        idx: int = 0
        while (idx < num_of_args or inf_args) and cursor < len(tokens) - 1:
            cursor += 1

            # Find type of current expected argument
            if not inf_args and num_of_args > 1:
                logging.info(
                    f"Expecting next argument to be of type {args[token][idx]}"
                )
                argument = args[token][idx]

            # Expected argument but got flag
            if tokens[cursor].startswith("-"):
                if inf_args:
                    cursor -= 1
                    logging.info(f"Found all arguments pertaining to flag {token}")
                    break

                logging.error(
                    f"Not enough arguments supplied to flag '{token}', flag '{tokens[cursor]}' followed"
                )
                success = False
                break

            # Cast argument to expected type
            try:
                cast_arg: Any = argument(tokens[cursor])

                # Add found argument to output dictionary
                if argument == list:
                    new_args[token].append(cast_arg)
                if argument == tuple:
                    new_args[token].add(cast_arg)
                else:
                    new_args[token] = cast_arg

                logging.info(f"Argument '{cast_arg}' found for flag '{token}'")

            except ValueError as e:
                logging.error(
                    f"Wrong argument type for argument with value '{tokens[cursor]}', expected type of '{argument}' but got type '{type(tokens[cursor])}'"
                )
                success = False
                break

            idx += 1

        cursor += 1

    logging.info(f"Finished parsing input")
    return success, new_args


if __name__ == "__main__":

    # Setup testing arguments
    test_args = {"run-tests": bool}
    success, args = parse_args(sys.argv[1:], test_args)

    # Run test cases
    if success and args["run-tests"] == True:

        print("Entering Test Mode:\n ")
        tests_succeded: bool = True

        try:
            from tests import cases
        except ImportError:
            logging.error(" >> Could not import ./tests.py")
            exit()

        for enum, case in enumerate(cases):

            if case.name != None:
                print(f" --- '{case.name}' --- ")

            success, args = parse_args(case.inp, case.args)
            print(args)
            print(
                f"""\nTest case [{enum}] gave the following results:
> matching success expectations: {success == case.success},
> matching output expectations: {args == case.output}
            \n"""
            )
