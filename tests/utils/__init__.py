"""
This utility module contains functions that can be used to help check if the
proper files are present, run drivers on the student's code, and get the
results of the drivers

The below import statements are used to expose the functions in this module to
the rest of the tests
"""

from utils.file_checking import check_and_get_files
from utils.driver_running import run_program, Submission, compile_and_run
from utils.common import subprocess_run, ta_print

# Adding the functions to __all__ so they can be imported with
# from utils import *, and to make the linter happy
__all__ = [
    check_and_get_files,
    run_program,
    Submission,
    subprocess_run,
    compile_and_run,
    ta_print,
]
