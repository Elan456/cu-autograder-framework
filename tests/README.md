# Tests Folder

### `test.py`

The main testing file. It should contain all the Python unit tests used for grading.

### `utils`

A Python package containing modules with helper functions for testing. More info in the `utils/README.md` file.

### `drivers`

This is where you should put scripts that are used to test the student's code.
They will be copied into the source directory before testing, and will never be given read access to the "student" user.
For example, if you want to compile a `driver.c` file and run it with the student's code, you would put the `driver.c` file here.

### `io_files`

Put the files you want the student's code to be able to read and interact with here. Everything here will be copied
into the source directory before testing and given read access to the "student" user.
For example, if you want the student's code to read from a file called `input.txt`, you would put that file here.

## Security

Everything in the `tests` folder is owned by the "root" user and cannot be read by the "student" user. You can
safely store hidden test cases here in the `test.py` and `drivers` areas. The `io_files` directory is the only
exception to this rule, as each file is given read access to the "student" user after being copied into the 
source directory.


