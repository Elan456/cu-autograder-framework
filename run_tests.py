"""
This file is used to run all of the tests detected in the tests folder
All the results are then written to a results.json file which is used
to score the student.

It will also read the ta_print.txt file and print it out to the console
such that only TAs and instructors will be able to see the output on
Gradescope
"""

import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner


SETUP_CLASS_NAME = "Test01Setup"


def _iter_test_cases(suite):
    """Yield concrete test cases from a potentially nested suite."""
    for test in suite:
        if isinstance(test, unittest.TestSuite):
            yield from _iter_test_cases(test)
        else:
            yield test


def _prioritize_setup_suite(discovered_suite):
    """
    Move tests from Test01Setup to the front while preserving
    relative order for all tests.
    """
    setup_tests = []
    other_tests = []

    for test in _iter_test_cases(discovered_suite):
        if test.__class__.__name__ == SETUP_CLASS_NAME:
            setup_tests.append(test)
        else:
            other_tests.append(test)

    ordered_suite = unittest.TestSuite()
    ordered_suite.addTests(setup_tests)
    ordered_suite.addTests(other_tests)
    return ordered_suite


# This will run any testing scripts it can find and then writes all the results
# to the results.json
if __name__ == "__main__":
    discovered_suite = unittest.defaultTestLoader.discover("tests")
    suite = _prioritize_setup_suite(discovered_suite)
    with open("/autograder/results/results.json", "w", encoding="utf-8") as f:
        JSONTestRunner(visibility="visible", stream=f).run(suite)

    # Sending all of the ta_print information out
    with open(
        "/autograder/source/tests/ta_print.txt", "r", encoding="utf-8"
    ) as f:
        if f.read() != "":
            print("TA Print:")
            f.seek(0)
        print(f.read())
