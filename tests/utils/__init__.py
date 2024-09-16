"""
This utility module contains functions that can be used to help check if the
proper files are present, run drivers on the student's code, and get the
results of the drivers

The below import statements are used to expose the functions in this module to
the rest of the tests
"""


# flake8: noqa F401
from . import setup
from .driver_running import (
    run_program,
    Submission,
    compile_and_run,
    remove_main,
)
from .stdout_checking import phrases_out_of_order, check_phrases


from .common import subprocess_run, ta_print
