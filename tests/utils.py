import os 
import shutil
import time 
import subprocess

SOURCE_DIR = "/autograder/source"
SUBMISSION_DIR = "/autograder/submission" 

def check_and_get_files(required_files, optional_files, files_must_be_expected=True):
    """
    Moves expected files into the source directory 
    If an unexpected file is found or a required file is missing,
    then an expectation is raised. 
    
    required_files -- Files that must be in the submission
    optional_files -- Files that can be in the submission 
    files_must_be_expected -- Whether or not an exception should be raised if an unexpected file is found
    """
    
    # The files may be within a folder, so os.walk is used to find them
    submitted_files_names = []
    for root, dirs, files in os.walk(SUBMISSION_DIR):
        for file in files:
            # file is just the name of the file, not the path
            submitted_files_names.append(file)

    missing_files = []
    unexpected_files = []
    for required_file in required_files:
        if required_file not in submitted_files_names:
            missing_files.append(required_file)

    
    for submitted_file in submitted_files_names:
        if submitted_file not in required_files and submitted_file not in optional_files:
            unexpected_files.append(submitted_file)

    
    # If there are missing files or unexpected files, then raise an exception
    if len(missing_files) > 0:
        raise AssertionError("The following required files are missing: " + " ".join(missing_files))
    
    # If there are unexpected files, then raise an exception if files_must_be_expected is true
    if files_must_be_expected and len(unexpected_files) > 0:
        raise AssertionError("The following files were not asked for: " + " ".join(unexpected_files))

    
    # Copying the files into the source directory from the submission directory
    # All the files are copied in a flat manner (no folders)
    for root, _, files in os.walk(SUBMISSION_DIR):
        for file in files:
            shutil.copy(os.path.join(root, file), SOURCE_DIR)


# Class used to represent the result of a student's submission
class Submission:
    """
    output - string containing the program's output (stdout)
    errors - string containing the program's errors (stderr)
    timedout - True if the submission timed out during execution, False otherwise
    """

    output: str
    errors: str
    timedout: bool

    def __init__(self, output: str, errors: str, timedout: bool):
        self.output = output
        self.errors = errors
        self.timedout = timedout


def runProgram(
    executable: str,
    inputFile: str = None,
    txtContents: str = None,
    timeout: float = 0.1,
) -> Submission:
    """
    Run the specified executable with given input and return its output

    executable - string containing the name of the executable to run. 

    inputFile -     string containing the name of a text file containing
                    user input, separated by newlines. Default is `None`
    txtContents -   string containing the user input, separated by newlines.
                    Default is `None`.
    timeout -   float specifying how many seconds to wait before terminating
                the program. Default is 0.1
    """

    try:
        # Get user input as a stream of bytes, either from file specified by `inputFile` or from `txtContents`
        if inputFile:
            with open(inputFile, "r") as f:
                txtContents = bytes(f.read(), "ascii")
        elif txtContents:
            txtContents = bytes(txtContents, "ascii")

        time.sleep(1)  # Sometimes, not having this would result in test cases being unable to access the executable,
        # presumably because another test case was still running.

        # Run the code submission, use txtContents to serve as user input, and timeout after `timeout` seconds
        # 1subprocess.run()` returns a `CompletedProcess` object which contains the stdout and stderr
        results = subprocess.run(
            [executable],
            stdout=subprocess.PIPE,
            timeout=timeout,
            input=txtContents,
            user="student",
        )
        timedout = False

    # If submission times out, the TimeoutExpired object still contains the stdout and stederr,
    # so we can simply use the exception object as we would the CompletedProcess object
    except subprocess.TimeoutExpired as e:
        results = e
        timedout = True

    # If unexpected input is piped to program, stdout can often contain information in memory that goes past
    # the bounds of the file. To filter this out, we split the bytes string based on the location of ELF,
    # and only keep everything that was before ELF. This should result in only the submission's actual output
    # being displayed. This is not an issue with stderr.
    try:
        stdout = (
            ""
            if results.stdout is None
            else results.stdout.split(b"\x7fELF")[0].decode("utf-8")
        )
        stderr = "" if results.stderr is None else results.stderr.decode("utf-8")
    except UnicodeDecodeError:
        raise AssertionError("Could not decode your output to utf-8.\n"
                             "Make sure you don't output any invalid characters.")
    max_chars = 30000
    # If the standard output or error are longer than max_chars, truncate them
    truncationMessage = (
        f"\n\n** The output exceeded {max_chars} characters, so it was truncated **"
    )
    if len(stdout) > max_chars:
        stdout = stdout[:max_chars] + truncationMessage
    if len(stderr) > max_chars:
        stderr = stderr[:max_chars] + truncationMessage

    # Create a `Submission` object containing the results of the program's execution and return it
    submission = Submission(stdout, stderr, timedout)
    return submission


def removeMain(input_filename, output_filename):
    """
    Removes main from the input file and writes the result to the output file
    This can be used to later test individual functions without dealing with 
    multiple definitions of main. 
    """
    stack = []
    inside_main = False

    with open(input_filename, "r") as input_file:
        lines = input_file.readlines()

    with open(output_filename, "w") as output_file:
        for line in lines:
            # strip removes all whitespace at the beginning and end of the string
            stripped_line = line.strip()

            if stripped_line.startswith("int main(") or stripped_line.startswith(
                "int main ("
            ):
                inside_main = True

            if not inside_main:
                output_file.write(line)
            else:
                # Keeping track of the curly braces to only remove main 
                for char in line:
                    if char == "{":
                        stack.append(char)
                    elif char == "}":
                        if stack:
                            stack.pop()
                        if not stack:
                            inside_main = False


def compile_and_run(compilation_args, executable_name,
                    timeout=0.1) -> tuple[str, Submission]:
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
    if os.path.isfile(SOURCE_DIR + "/" + executable_name):
        submission = runProgram(
            executable=SOURCE_DIR + "/" + executable_name,
            timeout=timeout
        )
    else:
        # No executable file was created
        submission = None

    return compilation_errors, submission


