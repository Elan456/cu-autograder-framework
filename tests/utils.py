import os 

SOURCE_DIR = "/autograder/source"
SUBMISSION_DIR = "/autograder/submission"

def getFiles(required_files, optional_files):
    """
    Moves expected files into the source directory 
    If an unexpected file is found or a required file is missing
    a non-empty string will be returned explaining the error
    
    required_files -- Files that must be in the submission
    optional_files -- Files that can be in the submission 
    """
