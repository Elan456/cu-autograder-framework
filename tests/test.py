"""
This is the primary testing file which will hold all the test cases
that can contribute to the student's score.
"""

import time
import unittest  # Python's unit testing library
import os  # For moving files looking inside of folders
import utils  # Our custom utility package

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
    """
    Collection of test cases used to check and move files into the correct
    location and compile the main executable.
    """

    # Files that must be in their submission
    # They will fail the first test case if they don't have these files
    required_files = []  # TODO: Add the required files

    # Files that can be in their submission and should be
    # copied over. These could be extra credit files
    optional_files = []  # TODO: Add the optional files

    # If a submitted file is not a required or optional file, then
    # they will fail the first test case.
    # This helps reduce the number of extra files submitted by the student,
    # making it easier for the TAs to grade the correct files later

    # Copying all the files from the drivers folder into
    # the source directory, so we can use them to test the
    # student's code later
    # When the autograder is used, the cwd (i.e. the ".") is the
    # source directory (/autograder/source/)
    if os.path.isdir("tests/drivers") and len(os.listdir("tests/drivers")) > 0:
        os.system("cp -r tests/drivers/* .")

    @number("0.1")  # Does not affect execution order
    @weight(0)
    def test_01_check_files(self):
        """Expected files are present"""

        # Checking if the required files all exist and
        # no unexpected files were given
        # Moves the files into the source directory as well
        utils.check_and_get_files(self.required_files, self.optional_files)

        time.sleep(1)  # Gives a moment for the files to be moved over
        # and recognized by the system

    @number("0.2")
    @weight(0)
    def test_02_check_compile(self):
        """Main program compiles"""

        # What files should be created when the following command is run
        files_that_should_be_created = (
            []
        )  # TODO: Add the files that should be created

        # Tries to compile the student's main program
        # You could use the student's makefile
        # If all you want to test is individual functions, then you
        # wouldn't need to do this because you'll be compiling your
        # own drivers instead
        _, errors = utils.subprocess_run(["make"], "student")
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

        not_found_message = ""
        for file in files_that_should_be_created:
            if not os.path.isfile(os.path.join(os.getcwd(), file)):
                not_found_message += (
                    f"{file} was not created with your makefile's "
                    "default directive\n"
                )

        if not_found_message != "":
            raise AssertionError(not_found_message)


class Test02DirectOutputExample(unittest.TestCase):
    """
    Collection of test cases to test the direct output of the student's
    code with user input. Test03 shows how to test the functions directly.
    """

    def setUp(self):
        # Running the student's code and saving the output and errors
        # This is run before all the test cases in this class

        # Compiling their code
        command = ["g++", "studentCode.cpp", "-Wall", "-o", "studentCode.out"]
        compile_stdout, compile_stderr = utils.subprocess_run(
            command, "student"
        )
        command_string = " ".join(
            command
        )  # Looks like "g++ studentCode.cpp -Wall -o studentCode.out"

        # If there are compilation errors, then you can fail all the test cases
        # within this class
        if compile_stderr != "":
            utils.ta_print(
                f"Compile errors for {command_string}`: " + compile_stderr
            )
            raise AssertionError(f"Failed to compile with `{command_string}`")

        # Running the student's code with different inputs
        self.run1 = utils.run_program("studentCode.out", txtContents="1\n2\n")
        self.run2 = utils.run_program("studentCode.out", txtContents="3\n4\n")

    def test_01_menu_output(self):
        """Menu output"""
        # Checking for certain phrases in the output
        expected_phrases = [
            "1. Add",
            "2. Subtract",
            "3. Multiply",
            "4. Divide",
        ]
        # Getting which phrases are missing out-of-order
        # Returns the indexes of the phrases not found
        out_of_order = utils.phrases_out_of_order(
            expected_phrases, self.run1.output
        )

        # If a phrase is missing, then you can give a helpful error message
        if len(out_of_order) > 0:
            raise AssertionError(
                "The following phrases are missing or out of order: "
                + "\n".join([expected_phrases[i] for i in out_of_order])
            )


class Test03DirectFunctionExample(unittest.TestCase):
    """
    Collection of test cases to test functions called in
    the exampleDriver.cpp file
    """

    def setUp(self):
        # This is run before every test case in this class
        # You can use this to run the drivers on the student's code
        # and save the output and errors to self.submission which can be used
        # throughout the class. Each test case can then look for different
        # things within the output and award points accordingly.

        # Compiling and running the testing driver on the student's code
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
        signatures_of_functions_being_tested = "void example(char *)"
        if compile_errors != "":
            # Printing the details of the compiler errors such that only TAs
            # and instructors can easily view it. If this driver has hidden
            # tests, then you shouldn't show the compiler errors directly to
            # the student
            utils.ta_print(
                "Compile errors for "
                f"`{signatures_of_functions_being_tested}`: "
                f"{compile_errors}"
            )

            # This could also be a good place to provide the desired function
            # signatures to the student
            raise AssertionError(
                "Failed to compile a driver to test "
                f"`{signatures_of_functions_being_tested}`. "
                "Make sure you match the function signatures"
                " given in the directions"
            )

        # Checking that the end of the testing script was reached
        if "Case finished pass" not in self.submission.output:
            # Only printing rather than raising an exception because
            # they could still get points for the test cases that did run
            print(
                "The testing driver did not finish. This is usually caused by"
                " either an infinite loop or a segmentation fault. Some of the"
                " later test cases in this group may not have run."
            )

    @number("3.1")
    @weight(1)
    def test_simple_example(self):  # <- The word test is required in the name
        """Simple example test case"""  # <- The name that will be shown

        expected_outputs = ["Case 3+3=6 pass"]
        msg = ""

        # Checking that the expected output is in the student's output
        for i, expected_output in enumerate(expected_outputs):
            if expected_output not in self.submission.output:
                # Giving a helpful error message to the student relevant to
                # the outputs being checked
                if i == 0:  # i is the index of the expected output
                    # you could give different messages
                    # for different indexes not found
                    msg += (
                        "Code failed to add two single digit positive"
                        " integers together correctly. "
                    )

    # Partial credit docs:
    # https://github.com/gradescope/gradescope-utils/blob/0e642eff3bbc9bc86a7c2b9b9677f4c491d76beb/gradescope_utils/autograder_utils/decorators.py#L120C7-L120C21
    @number("3.2")
    @partial_credit(4)
    def test_multi_example(self, set_score=None):
        """Adding integers of different sizes"""

        # Looking for many outputs and giving partial credit for each one
        # found. This strategy can be used to avoid having too many test cases
        # on Gradescope.
        expected_outputs = [
            "Case 3+3=6 pass",
            "Case 1+8=9 pass",
            "Case 100+500=600 pass",
            "Case 1+1=2 pass",
        ]
        msg = ""  # Starting with a blank message to build on
        score = 0
        for i, expected_output in enumerate(expected_outputs):
            if expected_output not in self.submission.output:
                # The first two could be visible while
                # the last two are hidden
                if i < 2:
                    # Giving details about what numbers were used
                    msg += expected_output.split(" ")[1] + " failed\n"
                else:
                    # Not giving details about what numbers were used
                    msg += "Hidden case failed\n"
            else:
                score += 1

        # The set_score function is passed in by Gradescope
        set_score(score)
        if msg != "":
            # Adding extra info to the message
            msg += "\nFailed to add integers of different sizes together."
            raise AssertionError(msg)


class Test04UsingFileExample(unittest.TestCase):
    """
    Example of how to test the student's code when they must read from
    a file and also write to a file
    Must put the input file you want them to use in the drivers folder

    This example uses the `exampleInputFile.txt` in the drivers folder
    """

    def setUp(self):
        #  Because the input file is in the drivers folder, we know it
        #  will already be copied into the source directory when the autograder
        #  is run

        # First we need to give permissions to the student to read the file,
        # so we can still run their code as the student user, and it will be
        # able to use the file properly
        os.chmod("exampleInputFile.txt", 0o644)

        # Running the student's code and saving the output and errors
        # In this example, we assume the student's code takes in argument
        # -f to specify the input file
        self.stdout, self.stderr = utils.subprocess_run(
            ["./studentCode.out", "-f", "exampleInputFile.txt"], "student"
        )

        if self.stderr != "":
            utils.ta_print(
                "Error running when using exampleInputFile.txt: " + self.stderr
            )
            raise AssertionError(
                "Errors were encountered when trying to use an input file"
            )

    @weight(1)
    @number("4.1")
    def test_41_correct_stdout(self):
        """Using input file gives correct stdout"""
        expected_output = "The output of the student's code"
        if expected_output not in self.stdout:
            raise AssertionError(
                "The student's code did not output the expected output"
            )

    @weight(1)
    @number("4.2")
    def test_42_output_file(self):
        """Using input file gives correct output file"""
        # If the student's code is supposed to write to a file,
        # then we can check the contents of the file after running
        # the student's code

        # Opening the file and checking the contents
        with open("exampleOutputFile.txt", "r") as f:
            output = f.read()
            if "The expected output of the student's code" not in output:
                raise AssertionError(
                    "The student's code did not output the expected "
                    "output to the file"
                )
