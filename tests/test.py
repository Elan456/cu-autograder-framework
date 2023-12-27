"""
This is the primary testing file which will hold all the test cases
that can contribute to the student's score.
"""

import unittest  # Python's unit testing library
import os  # For moving files looking inside of folders
import utils
import time

# All of Gradescope's special decorators to modify
# how the tests are weighted and displayed
from gradescope_utils.autograder_utils.decorators import (
    # visibility,
    weight,
    number,
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

    @number("0.1")  # Does not affect execution order
    @weight(0)
    def test_checkFiles(self):
        """Expected files are present"""

        # Checking if the required files all exist and
        # no unexpected files were given
        # Moves the files into the source directory as well
        utils.check_and_get_files(self.required_files, self.optional_files)

        # Copying all the files from the drivers folder into
        # the source directory, so we can use them to test the
        # student's code later
        os.system("cp -r drivers/* source/")

        time.sleep(1)  # Gives a moment for the files to be moved over
        # and recognized by the system

    @number("0.2")
    @weight(0)
    def test_checkCompile(self):
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
