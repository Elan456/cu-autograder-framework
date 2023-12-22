"""
This is the primary testing file which will hold all of the test cases 
that can contribute to the student's score. 
"""

import unittest  # Python's unit testing library
import os  #  For moving files looking inside of folders
import subprocess  #  For running executables and saving their stdout

# All of Gradescope's special decorators to modify how the tests are weighted and displayed
from gradescope_utils.autograder_utils.decorators import visibility, weight, number, leaderboard


class test01_setup(unittest.TestCase):

    # Files that must be in their submission
    # They will fail the first test case if they don't have these files
    required_files = []

    # Files that can be in their submission and should be 
    # copied over. These could be extra credit files
    optional_files = []

    # If a submitted file is not a required or optional file, then 
    # they will fail the first test case 


    @number("0") # Does not affect execution order 
    @weight(0)
    def test_checkFiles(self):
        """Expected files are present"""

        # Checking if the required files all exist


