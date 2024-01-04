"""
This file contains functions and global constants used across multiple of
the utility modules
"""

import subprocess

SOURCE_DIR = "/autograder/source"  # This is also the cwd for the autograder
SUBMISSION_DIR = "/autograder/submission"


def ta_print(message: str) -> None:
    """
    Saves the message to a file to be read and printed by the autograder later
    If it's printed directly then it will be captured and shown with a test
    case for students to see instead.

    This output will be shown only to TAs and not to students
    """

    with open("/autograder/source/tests/ta_print.txt", "a") as ta_print_file:
        ta_print_file.write(message + "\n")


def subprocess_run(args: list[str]) -> tuple[str, str]:
    """
    Runs the given arguments in a subprocess and returns the output and errors
    from stdout and stderr

    If you want to run an executable, it's better to use the run_program
    function in driver_running.py, so you can add a timeout and user input

    args -  List of strings to use to run
                        e.g. ["g++", "formattingTest.cpp", "studentCode.cpp",
                              "-Wall", "-o", "formattingTest.out"]

                        e.g. ["./formattingTest.out"]  -- To run an executable,
                         better to use run_program

    """

    process = subprocess.Popen(
        args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    output = process.stdout.read().strip().decode("utf-8")
    errors = process.stderr.read().strip().decode("utf-8")
    process.stdout.close()
    process.stderr.close()
    process.kill()
    process.terminate()

    return output, errors
