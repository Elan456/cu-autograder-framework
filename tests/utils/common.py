"""
This file contains functions and global constants used across multiple of
the utility modules
"""

import subprocess
import os

SOURCE_DIR = "/autograder/source"  # This is also the cwd for the autograder
SUBMISSION_DIR = "/autograder/submission"

# Creating an empty ta_print.txt file
with open("/autograder/source/tests/ta_print.txt", "w") as ta_print_file:
    ta_print_file.write("")

# Removing read access from non-root users to ta_print.txt
os.chmod("/autograder/source/tests/ta_print.txt", 0o600)  # 6 is rw for owner


def ta_print(*args) -> None:
    """
    Saves the message to a file to be read and printed by the autograder later
    If it's printed directly then it will be captured and shown with a test
    case for students to see instead.

    Use the same way as print()

    This output will be shown only to TAs and instructors; not to students
    """

    message = ""
    for arg in args:
        message += str(arg) + " "

    with open("/autograder/source/tests/ta_print.txt", "a") as ta_print_file:
        ta_print_file.write(message + "\n")


def subprocess_run(
        args: list[str], user: str, timeout=None
) -> tuple[str, str]:
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
    user -  The user to run the program as (e.g. "student" or "root")
            Use "student" if you are running any code or file written
            by the students. Use "root" only when compiling drivers.
    timeout - How long the program can run for in seconds

    """
    try:
        process = subprocess.run(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            user=user,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as e:
        process = e
        return "", "Timeout expired"

    # If unexpected input is piped to program, stdout can often contain
    # information in memory that goes past the bounds of the file. To filter
    # this out, we split the bytes string based on the location of ELF,
    # and only keep everything that was before ELF. This should result in
    # only the submission's actual output being displayed. This is not an
    # issue with stderr.
    try:
        stdout = (
            ""
            if process.stdout is None
            else process.stdout.split(b"\x7fELF")[0].decode("utf-8")
        )
        if process.stderr is None:
            stderr = ""
        else:
            stderr = process.stderr.decode("utf-8")

    # Sometimes students will output non-utf-8 characters often because of
    # going out of bounds in c-strings
    # This will catch that and given a somewhat helpful error message
    except UnicodeDecodeError:
        # Giving all the details to the TAs
        ta_print(
            "Trouble decoding output\n"
            f"stdout: {process.stdout}\n"
            f"stderr: {process.stderr}"
        )
        # Giving a more helpful message to the students
        raise AssertionError(
            "Could not decode your output to utf-8.\n"
            "Make sure you don't output any invalid characters."
        )
    max_chars = 30000  # You can change this number
    # If the standard output or error are longer than max_chars, truncate them
    truncation_message = (
            f"\n\n** The output exceeded {max_chars} characters, so it was "
            + "truncated **"
    )
    if len(stdout) > max_chars:
        stdout = stdout[:max_chars] + truncation_message
    if len(stderr) > max_chars:
        stderr = stderr[:max_chars] + truncation_message

    return stdout, stderr
