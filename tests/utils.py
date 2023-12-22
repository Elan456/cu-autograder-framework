import os 
import shutil

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
    for root, dirs, files in os.walk(SUBMISSION_DIR):
        for file in files:
            shutil.copy(os.path.join(root, file), SOURCE_DIR)
