""" """

import sys
from rapidy import parse_args


if __name__ == "__main__":

    decl_args = {"drink": [str, int]}

    success, args = parse_args(sys.argv[1:], decl_args, silent=False)