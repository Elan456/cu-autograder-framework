"""
Monkey Patching the Utility functions to add Auto Hinting capabilities.
https://www.geeksforgeeks.org/monkey-patching-in-python-dynamic-behavior/

When these utilities are called, their arguments/outputs are recorded
into the AutoHint object automatically.
"""

import utils
from utils.auto_hint import AutoHint

# Keep references to the original, unpatched functions
_original_run_program = utils.run_program
_original_subprocess_run = utils.subprocess_run
_original_compile_and_run = utils.compile_and_run
_original_check_and_get_files = utils.setup.check_and_get_files
_original_phrases_out_of_order = utils.phrases_out_of_order
_original_check_case_pass = utils.check_case_pass

# Global reference to the current hinter
_current_hinter = None


def set_current_hinter(hinter: AutoHint):
    """
    Sets the global hinter for our patched functions to use.
    Call this before patching if you want your test to log
    to a specific hinter.
    """
    global _current_hinter
    _current_hinter = hinter


def get_current_hinter() -> AutoHint:
    """
    Retrieves the current global hinter.
    Returns None if no hinter has been set.
    """
    return _current_hinter


def patched_run_program(*args, **kwargs):
    """
    Wrapped version of utils.run_program that logs to the AutoHint.

    Signature in utils:
        def run_program(exec_file, txt_contents="",
                        input_file="", timeout=5, ...)

    We capture txt_contents and input_file if present,
    then call the original function.
    """
    ah = get_current_hinter()
    if ah:
        input_text = kwargs.get("txt_contents", "")
        if input_text:
            ah.add_test_user_input(input_text, context="Program input")

        input_file = kwargs.get("input_file", "")
        if input_file:
            ah.add_file(input_file, context="Program user input file")

    # Actually call the real run_program
    result = _original_run_program(*args, **kwargs)

    if ah:
        # Log the output
        ah.add_student_output(result.output, context="Run program output")
        if result.timed_out:
            ah.add_timed_out(context="Program timed out")

    return result


def patched_subprocess_run(*args, **kwargs):
    """
    Wrapped version of utils.subprocess_run that logs to the AutoHint.

    Signature in utils:
        def subprocess_run(cmd_list, user="student", timeout=...):
            returns (stdout_str, stderr_str)

    We capture the command list and any resulting stdout or stderr.
    """
    ah = get_current_hinter()
    if ah:
        # Safely parse the command list, if provided
        cmd = args[0] if args and isinstance(args[0], (list, tuple)) else []
        ah.add_shell_command(
            " ".join(cmd), context="Shell command executed on autograder"
        )

        # Check for any .cpp, .py, or .h files in the command list
        for arg in cmd:
            if (
                arg.endswith(".cpp")
                or arg.endswith(".py")
                or arg.endswith(".h")
            ):
                ah.add_file(arg, context="File used in shell command")

    # Actually call the real function
    stdout, errors = _original_subprocess_run(*args, **kwargs)

    # Capture compile or runtime errors
    if ah:
        if errors:
            ah.add_compile_error_message(errors)
        if stdout:
            ah.add_student_output(stdout, context="Shell command output")

    return stdout, errors


def patched_compile_and_run(*args, **kwargs):
    """
    Wrapped version of utils.compile_and_run that logs to the AutoHint.
    (Signature might be something like:
        def compile_and_run(compilation_args,
                            executable_name, timeout=0.1) -> (str, Submission)
    )

    Note that compile_and_run might internally call run_program,
    so you could see logs from both.
    We focus on logging the compile step here.
    """
    ah = get_current_hinter()
    if ah:
        # The first positional arg is typically the compilation_args list
        compilation_args = (
            args[0] if args and isinstance(args[0], (list, tuple)) else []
        )
        ah.add_shell_command(
            " ".join(compilation_args),
            context="Compilation command executed on autograder",
        )

        # Check for any .cpp, .py, or .h files in the compilation args
        for arg in compilation_args:
            if (
                arg.endswith(".cpp")
                or arg.endswith(".py")
                or arg.endswith(".h")
            ):
                ah.add_file(arg, context="File used in compilation")

    # Call the real function
    result = _original_compile_and_run(*args, **kwargs)
    return result


def patched_check_and_get_files(*args, **kwargs):
    """
    Wrapped version of utils.setup.check_and_get_files
    that logs to the AutoHint.

    Signature:
        def check_and_get_files(required_files, optional_files,
                                files_must_be_expected=True)

    We'll log which files are required/optional.
    """
    ah = get_current_hinter()
    if ah:
        required_files = (
            args[0] if len(args) > 0 and isinstance(args[0], list) else []
        )
        optional_files = (
            args[1] if len(args) > 1 and isinstance(args[1], list) else []
        )
        ah.add_file(
            ", ".join(required_files),
            context="Required files for the test case",
        )
        ah.add_file(
            ", ".join(optional_files),
            context="Optional files for the test case",
        )

    return _original_check_and_get_files(*args, **kwargs)


def patched_phrases_out_of_order(*args, **kwargs):
    """
    Wrapped version of utils.phrases_out_of_order that logs to the AutoHint.

    Signature:
        def phrases_out_of_order(expected_phrases,
                                 mother_string)
                                 -> list of missing phrase indexes

    We'll log each expected phrase and the student's output,
    then note which phrases are missing.
    """
    ah = get_current_hinter()
    # If we have a hinter, log the expected phrases and the student's output
    if ah:
        expected_phrases = (
            args[0] if len(args) > 0 and isinstance(args[0], list) else []
        )
        mother_string = (
            args[1] if len(args) > 1 and isinstance(args[1], str) else ""
        )
        for p in expected_phrases:
            ah.add_expected_phrase(
                p, context="Expected phrase to look for in the output"
            )
        ah.add_student_output(
            mother_string, context="Student's output to search for phrases"
        )

    # Actually call the real function
    result = _original_phrases_out_of_order(*args, **kwargs)

    # If any missing phrases, log that info
    if ah:
        expected_phrases = (
            args[0] if len(args) > 0 and isinstance(args[0], list) else []
        )
        for missing_idx in result:
            # Safety check in case missing_idx is out of range
            if missing_idx < len(expected_phrases):
                phrase = expected_phrases[missing_idx]
                ah.add_missing_phrase(
                    phrase, context="Missing phrase in the student's output"
                )

    return result


def patched_check_case_pass(*args, **kwargs):
    # Case name and driver output are the two args
    """
    Wrapped version of utils.check_case_pass that logs to the AutoHint.
    Signature:
        def check_case_pass(case_name: str, sub_output: str) -> bool
    """

    ah = get_current_hinter()
    # If we have a hinter, log the case name and the student's output
    if ah:
        case_name = (
            args[0] if len(args) > 0 and isinstance(args[0], str) else ""
        )
        sub_output = (
            args[1] if len(args) > 1 and isinstance(args[1], str) else ""
        )
        ah.add_hint_element(
            case_name, context="Test case name used by the testing driver"
        )
        ah.add_student_output(
            sub_output, context="Driver output to check for test case"
        )

    # Actually call the real function
    result = _original_check_case_pass(*args, **kwargs)
    # If the test case passed, log that info
    if ah and result:
        ah.add_hint_element(
            case_name, context="Test case passed", relevance=0.5
        )
    return result


def patch_utils():
    """
    Activates monkey patching by replacing the relevant utils functions
    with our patched versions.
    This should generally be called before running tests
    that you want logged to AutoHint.
    """
    utils.run_program = patched_run_program
    utils.subprocess_run = patched_subprocess_run
    utils.compile_and_run = patched_compile_and_run
    utils.setup.check_and_get_files = patched_check_and_get_files
    utils.phrases_out_of_order = patched_phrases_out_of_order
    utils.check_case_pass = patched_check_case_pass


def unpatch_utils():
    """
    Deactivates monkey patching by restoring the original functions.
    Call this after tests to avoid side effects in other code.
    """
    utils.run_program = _original_run_program
    utils.subprocess_run = _original_subprocess_run
    utils.compile_and_run = _original_compile_and_run
    utils.setup.check_and_get_files = _original_check_and_get_files
    utils.phrases_out_of_order = _original_phrases_out_of_order
    utils.check_case_pass = _original_check_case_pass
