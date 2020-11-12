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


    log = open("../tests.log", 'w')
    log.write(f"Date: {str(datetime.today())}")

    results = dict()

    for case in cases:
        logging.info(f"Running test case [{case.id}]")

        success = False
        args = {}
        try:
            success, args = corree.parse(case.input, case.definitions)
            logging.info("> Test succeeded")
        except Exception as e:
            logging.warning("> Test failed")
            pass

        log.write(f"Case [{case.id}]:\nreturned with status '{success}'\nand args: {args}\n")

    logging.info(f"Finished testing using [{len(cases)}] test cases")
    log.close()

