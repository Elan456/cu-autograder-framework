"""
This is the primary testing file which will hold all the test cases
that can contribute to the student's score.
"""

import unittest  # Python's unit testing library
import os  # For moving files looking inside of folders
import utils  # Our custom utility package
import time

# All of Gradescope's special decorators to modify
# how the tests are weighted and displayed
from gradescope_utils.autograder_utils.decorators import (
    # visibility,
    weight,
    number,
    partial_credit,
    # leaderboard,
)


class Test01Setup(unittest.TestCase):
    # Files that must be in their submission
    # They will fail the first test case if they don't have these files
    required_files = []

    # Files that can be in their submission and should be
    # copied over. These could be extra credit files
    optional_files = []

    # If a submitted file is not a required or optional file, then
    # they will fail the first test case.
    # This helps reduce the number of extra files submitted by the student,
    # making it easier for the TAs to grade the correct files later

    # Copying all the files from the drivers folder into
    # the source directory, so we can use them to test the
    # student's code later
    # When the autograder is used, the cwd is the source directory
    os.system("cp -r tests/drivers/* .")

    @number("0.1")  # Does not affect execution order
    @weight(0)
    def test_01_checkFiles(self):
        """Expected files are present"""

        # Checking if the required files all exist and
        # no unexpected files were given
        # Moves the files into the source directory as well
        utils.check_and_get_files(self.required_files, self.optional_files)

        time.sleep(1)  # Gives a moment for the files to be moved over
        # and recognized by the system

    @number("0.2")
    @weight(0)
    def test_02_checkCompile(self):
        """Main program compiles"""

        # Tries to compile the student's main program
        # You could use the student's makefile
        # If all you want to test is individual functions, then you
        # wouldn't need to do this because you'll be compiling your
        # own drivers instead

        output, errors = utils.subprocess_run(["make"])
        # Other example:
        # output, errors = utils.subprocess_run(["g++", "main.cpp",
        #                       "object.cpp", "-Wall", "-o", "main.out"])

        # Display errors if there are any
        # Because this doesn't interact with any of our hidden drivers,
        # it's okay to show the student's output
        if errors != "":
            msg = (
                "Errors when compiling using your makefile's"
                " default directive: " + errors
            )

            # At this point, you can add extra info to the message
            # if you want to reiterate any important directions relevant to
            # passing this test case
            msg += ""
            raise AssertionError(msg)

        # What files should be created when the student's makefile is run
        files_that_should_be_created = []
        not_found_message = ""
        for file in files_that_should_be_created:
            if not os.path.isfile(os.path.join(os.getcwd(), file)):
                not_found_message += (
                    f"{file} was not created with your makefile's "
                    "default directive\n"
                )

        if not_found_message != "":
            raise AssertionError(not_found_message)


class Test02FunctionalityExample(unittest.TestCase):
    def setUp(self):
        # This is run before every test case in this class
        # You can use this to run the drivers on the student's code
        # and save the results to self.submission

        compile_errors, self.submission = utils.compile_and_run(
            [
                "g++",
                "exampleDriver.cpp",
                "studentCode.cpp",  # Linking the student's code
                "-o",
                "exampleDriver.out",
            ],
            "exampleDriver.out",
        )

        # If there are compilation errors, then you can fail all the test cases
        # within this class
        signatures_of_functiones_being_tested = "void example(char *)"
        if compile_errors != "":
            # Printing the details of the compiler errors such that only TAs
            # and instructors can easily view it. If this driver has hidden
            # tests, then you shouldn't show the compiler errors directly to
            # the student
            utils.ta_print(
                "Compile errors for "
                f"{signatures_of_functiones_being_tested}: "
                f"{compile_errors}"
            )

            # This could also be a good place to provide the desired function
            # signatures to the student
            raise AssertionError(
                "Failed to compile a driver to test "
                f"{signatures_of_functiones_being_tested}. "
                "Make sure you match the function signatures"
                " given in the directions"
            )

        # Checking that the end of the testing script was reached
        if "Case finished pass" not in self.submission.output:
            # Only printing rather than raising an exception because
            # they could still get points for the test cases that did run
            print(
                "The testing driver did not finish. This is usually caused by"
                "either an infinite loop or a segmentation fault. Some of the"
                "later test cases in this group may not have run."
            )

    @number("1.1")
    @weight(1)
    def testSimpleExample(self):
        """Simple example test case"""  # <- The name that will be shown

        expected_outputs = ["Case 3+3=6 pass"]

        for i, expected_output in enumerate(expected_outputs):
            if expected_output not in self.submission.output:
                raise AssertionError(
                    "Code failed to add two single digit positive integers "
                    "together correctly. "
                )

    # Partial credit docs:
    # https://github.com/gradescope/gradescope-utils/blob/0e642eff3bbc9bc86a7c2b9b9677f4c491d76beb/gradescope_utils/autograder_utils/decorators.py#L120C7-L120C21
    @number("1.2")
    @partial_credit(3)
    def testMultiExample(self, set_score=None):
        """Adding integers of different sizes"""

        expected_outputs = [
            "Case 3+3=6 pass",
            "Case 1+8=9 pass",
            "Case 100+500=600 pass",
        ]
        msg = ""
        score = 0
        for i, expected_output in enumerate(expected_outputs):
            if expected_output not in self.submission.output:
                msg += "Hidden case failed"
            else:
                score += 1

        set_score(score)
        if msg != "":
            # Adding extra info to the message
            msg += "\nFailed to add integers of different sizes together."
            raise AssertionError(msg)
