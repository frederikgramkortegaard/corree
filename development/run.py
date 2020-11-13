""" Runs the following test suite on the Corree version seen in the development/src/ folder """

import os
import sys

sys.path.append("src")

import corree
import logging

logging.basicConfig(level=logging.DEBUG)

from typing import *
from datetime import datetime
from testcases import cases

if __name__ == "__main__":
    logging.info("Running tests on development version of Corree")    


    log = open("tests.log", 'w')
    log.write(f"Date: {str(datetime.today())}\n\n")

    results = dict()
    
    failed: int = 0

    for enum, case in enumerate(cases):
        logging.info(f"Running test case #[{enum + 1}]")
        success, args = corree.parse(case.input, case.definitions)

        if success != case.success or args != case.output:
            logging.warning("> Test failed")
            failed += 1
        else:

            logging.info("> Test succeeded")

        log.write(f"Case [{enum + 1}]:\n> was given input: '{case.input}'\n> was given definitions: '{case.definitions}'\n> returned with status '{success}'\n> returned with parsed args: {args}\n")

    log.write(f"{failed}/{len(cases)} Tests failed")
    
    logging.info(f"Finished testing using [{len(cases)}] test cases")
    if failed != 0:
        logging.info(f"{failed} out of {len(cases)} cases were not successful, see tests.log for more information") 
    else:
        logging.info("All tests were successful")
    log.close()

    print(failed == 0)
