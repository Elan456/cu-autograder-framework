"""
This is the primary testing file that will hold all the test cases
that can contribute to the student's score.

Read the tests/README.md file for more information on this file and
how it works.
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
    # If a file is missing, then they will fail the first test case
    required_files = [
        "studentMain.cpp",
        "studentFuncs.cpp",
        "studentFuncs.h",
        "makefile",
    ]  # TODO: Replace with actual files

    # Files that can be in their submission and should be
    # copied over. These could be extra credit files
    optional_files = []  # TODO: Add the optional files

    # If a submitted file is not a required or optional file, then
    # they will fail the first test case.
    # This helps reduce the number of extra files submitted by the student,
    # making it easier for the TAs to grade the correct files later

    # Grabbing all the drivers and io_files and moving them into the source
    # directory where the student's code can interact with them
    utils.setup.move_drivers_to_source()
    utils.setup.move_io_files_to_source()

    @number(
        "0.1"
    )  # Does not affect execution order, what's displayed in Gradescope
    @weight(0)
    def test_01_check_files(self):
        """Expected files are present"""

        # Checking if the required files all exist in the
        # submission directory and that no unexpected files were given
        # Moves the expected files into the source directory
        # Will raise an exception if an unexpected file is found
        utils.setup.check_and_get_files(
            self.required_files, self.optional_files
        )

        time.sleep(1)  # Gives a moment for the files to be moved over
        # and recognized by the system

    @number("0.2")
    @weight(0)
    def test_02_check_compile(self):
        """Main program compiles"""

        # What files should be created when the following command is run
        files_that_should_be_created = [
            "studentMain.out"
        ]  # TODO: Add the files that should be created

        # Runs the "make" command as the "student" user
        # The "student" user has restricted permissions
        # Collects the errors from running the command
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

        # After the compilation, we can check if the expected files
        # were created.
        # We'll build a message to show the student if any files were missing
        not_found_message = ""
        for file in files_that_should_be_created:
            if not os.path.isfile(os.path.join(os.getcwd(), file)):
                not_found_message += (
                    f"{file} was not created with your makefile's "
                    "default directive\n"
                )

        if not_found_message != "":
            raise AssertionError(not_found_message)


# TODO: Delete all the example test cases below and replace them with your own


class Test02DirectOutputExample(unittest.TestCase):
    """
    Collection of test cases to test the direct output of the student's
    code with user input. Test03 shows how to test the functions directly
    using drivers.
    """

    @number("2.1")
    @weight(1)
    def test_01_intro_output(self):
        """Intro output is correct"""

        # Running the compiled student's code with an input of 1, 2, and 1
        run = utils.run_program("./studentMain.out", txt_contents="1\n2\n1\n")

        # Checking for certain phrases in the output
        expected_phrases = [
            "Welcome to the calculator program!",
            "No input file given",
            "Defaulting to manual input",
        ]
        # Getting which phrases are missing or out-of-order
        # Returns the indexes of the phrases not found
        out_of_order = utils.phrases_out_of_order(expected_phrases, run.output)

        # If a phrase is missing, then you can give a helpful error message
        if len(out_of_order) > 0:
            raise AssertionError(
                "The following phrases are missing or out of order:\n "
                + "\n".join([expected_phrases[i] for i in out_of_order])
            )

    @number("2.2")
    @weight(1)
    def test_2_2_timeout(self):
        """Timeout test"""
        # This run should cause a timeout (the default timeout is 5 seconds)
        # this series of inputs will trigger a infinite loop in this example
        # code.
        run = utils.run_program("./studentMain.out", txt_contents="1\n2\n4\n")

        if not run.timed_out:
            raise AssertionError("The program did not timeout as expected")


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
                "exampleDriver.cpp",  # Your testing driver
                "studentFuncs.cpp",  # Linking the student's code
                "-o",
                "exampleDriver.out",
            ],
            "exampleDriver.out",
        )

        # If there are compilation errors, then you can fail all the test cases
        # within this class
        signatures_of_functions_being_tested = "int studentAdd(int, int)"
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
        """Checking driver output test"""  # <- The name that will be shown

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

        if msg != "":
            # Adding extra info to the message
            msg += "\nFailed to add simple integers together."
            raise AssertionError(msg)

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

        # Getting list of which outputs were not found
        # e.g. missing = [1, 3] means the second and
        # fourth outputs were not found
        missing = utils.phrases_out_of_order(
            expected_outputs, self.submission.output
        )
        msg = ""  # Starting with a blank message to build on

        # Calculating the score based on the number of outputs found
        score = len(expected_outputs) - len(missing)
        for m in missing:
            # For the first two cases, we'll give lots of details
            # For the last two cases, we'll just say that a hidden case
            # failed
            # This way, the student can't just hardcode for all 4 cases
            if m < 2:
                # Giving details about what numbers were used
                msg += expected_outputs[m].split(" ")[1] + " failed\n"
            else:
                # Not giving details about what numbers were used
                msg += "Hidden case failed\n"
        else:
            score += 1

        # The set_score function is passed in by Gradescope
        set_score(score)
        if msg != "":
            msg = "\n" + msg
            # Adding extra info to the message
            msg += "\nFailed to add integers of different sizes together."
            raise AssertionError(msg)

    @number("3.3")
    @weight(1)
    def test_func_in_main_example(self):
        """Directly calling a function defined in main"""

        # Create a version of the student's main
        # that doesn't have the main function
        utils.remove_main("studentMain.cpp", "studentMainNoMain.cpp")

        # Using the no main version of the student's code, we can
        # call the functions directly while avoiding multiple definitions
        # of main errors
        # using the exampleMainDriver.cpp
        compile_errors, sub = utils.compile_and_run(
            [
                "g++",
                "exampleMainDriver.cpp",
                "studentFuncs.cpp",
                "-o",
                "exampleMainDriver.out",
            ],
            "exampleMainDriver.out",
        )

        if compile_errors != "":
            utils.ta_print("Compile errors in 3.3: " + compile_errors)
            raise AssertionError("Failed to compile the main driver")

        if "Hello from studentMain.cpp" not in sub.output:
            raise AssertionError(
                "Your `say_hello()` function did not print the expected output"
            )


class Test04UsingFileExample(unittest.TestCase):
    """
    Example of how to test the student's code when they must read from
    a file and also write to a file
    Must put the input file you want them to use in the io_files folder

    This example uses the `exampleInputFile.txt` in the io_files folder
    """

    def setUp(self):
        # Because exampleInputFile.txt is in the io_files folder, we know it
        # will already be copied into source and given read permission to the
        # student

        # Running the student's code and saving the output and errors
        # In this example, we assume the student's code takes in argument
        # -f to specify the input file
        self.stdout, self.stderr = utils.subprocess_run(
            ["./studentMain.out", "-f", "exampleInputFile.txt"], "student"
        )

        if self.stderr != "":
            # Giving the TA's all the details of the error message
            utils.ta_print(
                "Error running when using exampleInputFile.txt: " + self.stderr
            )
            raise AssertionError(
                "Errors were encountered when trying to use an input file"
            )

    @weight(1)
    @number("4.1")
    def test_41_correct_stdout_example(self):
        """Using input file gives correct stdout"""
        expected_output = [
            "Welcome to the calculator program!",
            "Output has been written to output.txt",
        ]

        missing = utils.phrases_out_of_order(expected_output, self.stdout)
        if len(missing) > 0:
            raise AssertionError(
                "The following phrases are missing or out of order:\n "
                + "\n".join([expected_output[i] for i in missing])
            )

    @weight(1)
    @number("4.2")
    def test_42_output_file_example(self):
        """output.txt has the correct values"""
        # If the student's code is supposed to write to a file,
        # then we can check the contents of the file after running
        # the student's code

        # Opening the file and checking the contents
        expected_output = "7\n5\n15"
        try:
            with open("output.txt", "r") as f:
                output = f.read()
                if expected_output not in output:
                    raise AssertionError(
                        "output.txt did not contain the expected "
                        " values. It contained: " + output
                    )
        except FileNotFoundError:
            raise AssertionError("output.txt was not created")
