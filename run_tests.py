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

# This will run any testing scripts it can find and then writes all the results
# to the results.json
if __name__ == "__main__":
    suite = unittest.defaultTestLoader.discover("tests")
    with open("/autograder/results/results.json", "w", encoding="utf-8") as f:
        JSONTestRunner(visibility="visible", stream=f).run(suite)

    # Sending all of the ta_print information out
    with open(
        "/autograder/source/tests/ta_print.txt", "r", encoding="utf-8"
    ) as f:
        print(f.read())
