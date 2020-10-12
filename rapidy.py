""" Easily define and parse command line arguments using dictionaries and types """

import re
import sys
import logging
from typing import *
from collections import defaultdict

logging.basicConfig(level=logging.DEBUG)

## TODO // Handle all iters dynamically instead of hardcoding list support


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
    success: bool = True
    inf_args: bool = False
    curser: int = 0

    # Set default bool value to be false
    for key, value in args.items():
        if value == bool:
            new_args[key] = False

    # Iterate through given tokens
    while curser < len(tokens):

        token = tokens[curser]

        # Handle arguments help request
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
            logging.error(
                f"token number [{curser}] with value '{token}' - is not expected as an argument, nor is it defined as a flag"
            )
            success = False
            break

        # Remove prefixed dashes from flag
        token = token[offset:]

        # Flag is not valid
        if token not in args:
            logging.error(f"flag '{token}' is not a valid option, see  --help")
            success = False
            break

        # Flag does not take multiple arguments
        if type(args[token]) != list:

            # Flag is a bool, don't look for arguments
            if args[token] == bool:
                logging.info(f"flag '{token}' is a bool, don't look for arguments")
                new_args[token] = True
                curser += 1
                continue

            logging.info(f"Flag '{token}' is only Looking for a single argument")
            num_of_args = 1

            # Set the expected argument type
            argument = args[token]

        # Flag takes more than a single arg
        elif type(args[token]) == list:

            num_of_args = len(args[token])

            # Flag takes any number of args
            if num_of_args == 1:
                inf_args = True
                logging.info(
                    f"Setting flag '{token}' to take infinite arguments of type {args[token][0]}"
                )
                argument = args[token][0]
            else:
                logging.info(f"Flag '{token}' takes more than a single argument")

        # Ensure enough arguments are supplied
        if num_of_args + curser >= len(tokens) and not inf_args:
            logging.error(f"Not enough arguments given to flag '{token}'")
            success = False
            break

        # Find argument(s) for flag
        idx: int = 0
        while (idx < num_of_args or inf_args) and curser < len(tokens) - 1:
            curser += 1

            # Find type of current expected argument
            if not inf_args and num_of_args > 1:
                logging.info(
                    f"Expecting next argument to be of type {args[token][idx]}"
                )
                argument = args[token][idx]

            # Expected argument but got flag
            if tokens[curser].startswith("-"):
                if inf_args:
                    curser -= 1
                    logging.info(f"Found all arguments pertaining to flag {token}")
                    break

                logging.error(
                    f"Not enough arguments supplied to flag '{token}', flag '{tokens[curser]}' followed"
                )
                success = False
                break

            # Cast argument to expected type
            try:

                cast_arg = argument(tokens[curser])
                new_args[token].append(cast_arg)

                logging.info(f"Argument '{cast_arg}' found for flag '{token}'")
                logging.info(f"Arguments for flag '{token}' are now {new_args[token]}")

            except ValueError as e:
                logging.error(
                    f"Wrong argument type for argument with value '{tokens[curser]}', expected type of '{argument}' but got type '{type(tokens[curser])}'"
                )
                success = False
                break

            idx += 1

        # Unpack Expected Single Arguments From List Wrapper
        if num_of_args == 1 and type(args[token]) != list:
            logging.info(f"Unpacking wrapped argument {args[token]}")
            new_args[token] = new_args[token][0]

        curser += 1

    # INCOMPLETE // hacky default value solutions
    for arg in args:
        if new_args[arg] == []:
            if type(args[arg]) == list:
                new_args[arg] = list()
            else:
                new_args[arg] = None

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
            print(
                f"""\nTest case [{enum}] gave the following results:
> matching success expectations: {success == case.success},
> matching output expectations: {args == case.output}
            \n"""
            )

            if success != case.success or args != case.output:
                tests_succeded = False

    if not tests_succeded:
        logging.error("TESTS WERE NOT SUCCESFULL")