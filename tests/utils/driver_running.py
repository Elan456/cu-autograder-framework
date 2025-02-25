"""
This file contains functions used to run a student's code
and return the results
"""

import subprocess
import time
import os
import utils.common as common
import utils.parsing as parsing


# Class used to represent the result of a student's submission
class Submission:
    """
    output - string containing the program's output (stdout)
    errors - string containing the program's errors (stderr)
    timed_out -  True if the submission timed out during execution,
                False otherwise
    """

    output: str
    errors: str
    timed_out: bool

    def __init__(self, output: str, errors: str, timed_out: bool):
        self.output = output
        self.errors = errors
        self.timed_out = timed_out


def run_program(
    executable: str,
    input_file: str = None,
    txt_contents: str = None,
    timeout: float = 5,
    user: str = "student",
) -> Submission:
    """
    Run the specified executable as the student user with given input and
    return its output

    executable - string containing the name or path of the executable to run.
                 E.g. "Program.out"

    inputFile -     string containing the name of a text file containing
                    user input, separated by newlines. Default is `None`
    txtContents -   string containing the user input, separated by newlines.
                    Default is `None`.
    timeout -   float specifying how many seconds to wait before terminating
                the program. Default is None
    user -      string specifying the user to run the program as. Default is
                "student"
    """

    try:
        # Get user input as a stream of bytes, either from file specified by
        # `inputFile` or from `txtContents`
        if input_file:
            with open(input_file, "r") as f:
                txt_contents = bytes(f.read(), "ascii")
        elif txt_contents:
            txt_contents = bytes(txt_contents, "ascii")

        time.sleep(1)  # Sometimes, not having this would result in test
        # cases being unable to access the executable,
        # presumably because another test case was still running.

        # If the executable has no path and doesn't have a ./, then add it
        if "/" not in executable and not executable.startswith("./"):
            executable = "./" + executable

        # Run the code submission, use txtContents to serve as user input,
        # and timeout after `timeout` seconds 1subprocess.run()` returns a
        # `CompletedProcess` object which contains the stdout and stderr
        results = subprocess.run(
            [executable],
            stdout=subprocess.PIPE,
            timeout=timeout,
            input=txt_contents,
            user=user,
        )
        timedout = False

    # If submission times out, the TimeoutExpired object still contains the
    # stdout and stederr, so we can simply use the exception object as we
    # would the CompletedProcess object
    except subprocess.TimeoutExpired as e:
        results = e
        timedout = True

    # If unexpected input is piped to program, stdout can often contain
    # information in memory that goes past the bounds of the file. To filter
    # this out, we split the bytes string based on the location of ELF,
    # and only keep everything that was before ELF. This should result in
    # only the submission's actual output being displayed. This is not an
    # issue with stderr.
    try:
        stdout = (
            ""
            if results.stdout is None
            else results.stdout.split(b"\x7fELF")[0].decode("utf-8")
        )
        if results.stderr is None:
            stderr = ""
        else:
            stderr = results.stderr.decode("utf-8")

    except UnicodeDecodeError:
        raise AssertionError(
            "Could not decode your output to utf-8.\n"
            "Make sure you don't output any invalid characters."
        )
    max_chars = 30000
    # If the standard output or error are longer than max_chars, truncate them
    truncation_message = (
        f"\n\n** The output exceeded {max_chars} characters, so it was "
        + "truncated **"
    )
    if len(stdout) > max_chars:
        stdout = stdout[:max_chars] + truncation_message
    if len(stderr) > max_chars:
        stderr = stderr[:max_chars] + truncation_message

    # Create a `Submission` object containing the results of the program's
    # execution and return it
    submission = Submission(stdout, stderr, timedout)
    return submission


def remove_main(input_filename, output_filename):
    """
    Removes main from the input C or C++ file and writes the result to the
    output file
    This can be used to later test individual functions without dealing with
    multiple definitions of main.
    """
    parsing.remove_functions(input_filename, output_filename, "main")


def compile_and_run(
    compilation_args, executable_name, timeout=0.1
) -> tuple[str, Submission]:
    """
    Returns the compilation errors and then the submission
    If there are compilation errors then the submission will be None
    The executable_name file must be in the source directory

    compilation_args -  List of strings to use to compile
                        e.g. ["g++", "formattingTest.cpp", "studentCode.cpp",
                              "-Wall", "-o", "formattingTest.out"]
    executable_name -   Name of the executable file to run
                        e.g. "formattingTest.out"
    timeout         -   How long the program can run for
    """

    compiler = subprocess.Popen(
        compilation_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    compilation_errors = compiler.stderr.read().strip().decode("utf-8")
    compiler.stdout.close()
    compiler.stderr.close()
    compiler.kill()
    compiler.terminate()

    # If compilation failed,
    # then the executable file will not be present in the source folder
    if os.path.isfile(common.SOURCE_DIR + "/" + executable_name):
        executable_path = common.SOURCE_DIR + "/" + executable_name
        submission = run_program(executable=executable_path, timeout=timeout)
    else:
        # No executable file was created
        submission = None

    return compilation_errors, submission
