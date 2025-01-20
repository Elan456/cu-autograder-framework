# Clemson University Autograder Framework 

Python-Based Generic Output Checking Autograder Framework for use with the 
[Gradescope](https://gradescope.com) autograder.

Originally based on the 
[General output-checking autograder example](https://gradescope-autograders.readthedocs.io/en/latest/diff_general/)
given by Gradescope.

# Usage
1. Download the latest release from the [releases page](https://github.com/Elan456/cu-autograder-framework/releases) 
or clone the repository
2. Place testing drivers in the `tests/drivers` directory
3. Place any input files that the student's code will need to read or edit in the `tests/io_files` directory
4. Put unit tests in the `tests/test.py` file which can use the drivers and io_files
5. Zip up the autograder: `sh zipper.sh` (The name of the zip file can be changed in the `zipper.sh` script)
6. Upload the autograder to Gradescope
7. Upload your sample code to Gradescope and see if everything works as expected

## Files (and what they do)

Even though many files are mentioned, the key file to change is the `test.py` file

* `setup.sh` - Run when the autograder docker image is built. This is where
  you should install any dependencies that your autograder needs and setup 
  users. You could compile code here, but it's easier to handle errors and 
  display them nicely if you compile in the `test.py` file. Also injects a
  checksum into the harness, preventing `run_autograder` from being overwritten
  by the student.  
* `run_autograder` - What Gradescope runs when the autograder is executed.
  This is typically used to start the Python test script.
* `run_tests.py` - Finds all the unit tests within the `tests` directory
  and runs them. It then logs the results to a `results.json`. 
  This shouldn't need to be changed. Typically, it just runs `test.py`
* `requirements.txt` - A list of Python packages that are installed
prior to the autograder running.
* `zipper.sh` - A small script that zips up the autograder for upload to 
  Gradescope.
* `example_sample_code/samplecode.zip` - Sample code which should pass
all the example test cases given in this framework

### Tests directory


| Directory        | Use                      | Function                                                                         |
|------------------|--------------------------|----------------------------------------------------------------------------------|
| `tests/drivers`  | Store drivers | Copied into the `source` folder **without giving** read access to the "student" user      |
| `tests/io_files` | Store input files        | Copied into the `source` folder and **granted** read access to the "student" user      |

* `test.py` - The Python script which compiles, runs, and observes drivers and
  the student's code. Examples are given in the file.
* `utils` - A Python package that contains custom utilities for the autograder.
  This is where to define functions that are used multiple times in the autograder.


# Security

While security was not the primary focus during the development of this framework, several precautions have been implemented to mitigate common attack vectors. These measures include preventing attempts by students to tamper with critical system files, such as tarring the root directory, capturing hidden test cases, or overwriting the `run_autograder` script to manipulate their scores.

Many of the utility functions in `utils` leverage a restricted "student" user with limited permissions. Provided that the student's code is not executed with root privileges, the contents within the `tests` directory should remain secure. However, further testing is recommended to ensure the robustness of these precautions.

Care should be taken when running student-provided makefiles without the "student" user, as they may be used to execute arbitrary commands on the system.

Security becomes increasingly critical as the number of students using the framework grows, making it more challenging to identify malicious submissions. For additional security considerations, [Gradescope's best practices](https://gradescope-autograders.readthedocs.io/en/latest/best_practices/) provide valuable guidelines. As an example, running a student's code as root while they have a malicious setup, such as [this](https://www.reddit.com/r/csMajors/comments/rlkf55/if_your_school_uses_gradescope_autograder_hidden/), may expose hidden test cases. 

# Contributing

## Feature Requirements

If you have a new feature you would like to add it to the framework, please ensure it meets the following 6 requirements:

1. **Reliable**  
   Everything built directly into the main framework must work consistently. This is meant to be a reliable baseplate for
   autograder developers.   
   We'll continue adding to the [example_sample_code](example_sample_code), so that 
   we can test new features.    
   **Experimental features** can be kept on separate branches or forks. 

2. **Modular**   
   It must be easy to include or exclude any feature. Don't force it on the developer,
   but if they want to use this feature, it should be easy to get to. This aligns with
   breaking things into multiple files and using Python's packaging system to stay
   organized and promote reusability.

3. **Documented**     
   How it works, when to use it, and what it does should be well documented.
   Add documentation to the [README.md](/tests/utils/README.md) in the utils directory,
   so new users can find your feature and understand when to use it. 

4. **Useful**    
   This feature should address a real problem and either save time or effort for the developer or students.

5. **Minimal Footprint**    
   Don't introduce unnecessary complexity. We want debugging student's submissions on the autograder
   to get easier, not harder. Autograders also need to build and run quickly. 

6. **Backwards Compatibility**      
   New features shouldn't break the old features.
   If an old feature needs to be removed, it should be replaced
   with a suitable alternative. 

## Making Changes

To contribute to this repository, follow one of the two workflows below:

### Option 1: Direct Contribution
1. Clone the repository:  
   `git clone <repository-url>`
2. Create a new branch for your changes:  
   `git checkout -b <branch-name>`
3. Implement your changes.
4. Commit your changes, ensuring all pre-commit hooks are satisfied:  
   `git commit -m "Description of changes"`
5. Push your branch to the repository:  
   `git push origin <branch-name>`
6. Create a pull request for review.
7. Wait for approval and feedback.
8. Once approved, merge your branch into the main branch.
9. Delete your branch after merging to keep the repository clean:  
   `git branch -d <branch-name>`
10. Celebrate!

### Option 2: Forking the Repository
1. Fork the repository by clicking the "Fork" button on GitHub.
2. Clone your forked repository:  
   `git clone <your-fork-url>`
3. Create a new branch for your changes:  
   `git checkout -b <branch-name>`
4. Implement your changes.
5. Commit your changes, ensuring all pre-commit hooks are satisfied:  
   `git commit -m "Description of changes"`
6. Push your changes to your fork:  
   `git push origin <branch-name>`
7. Create a pull request from your fork to the original repository for review.
8. Wait for approval and feedback.
9. Once approved, your changes will be merged into the original repository.
10. Keep your fork in sync with the original repository by pulling updates:  
   `git remote add upstream <original-repo-url>`  
   `git fetch upstream`  
   `git merge upstream/main`

By following either method, you can contribute effectively to the project.

### Pre-commit setup
This repository uses pre-commit hooks to ensure code quality and consistency. To set up pre-commit hooks, run the following command in the repository directory:

```bash
pip install pre-commit
pre-commit install
```

# Getting Help 
Feel free to email me at [ema8@clemson.edu](mailto:ema8@clemson.edu), or if you are a Clemson student,
message me on Teams to ask specific questions or set up a time to meet.

# Issues
If you find any issues, please report them on the issues page
of the repository. Please include as much information as possible
so that the issue can be reproduced and fixed.

# Feature Requests
If you have any feature requests, also use the issues
page of the repository. Please include as much information as possible
so that the feature can be implemented as requested.

