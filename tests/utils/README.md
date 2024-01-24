# Utilities Package

--------------------

Originally, the utilities were kept in a single `utils.py` file. However, as the
number of utilities grew, it became necessary to split them up into multiple
modules. This package contains all the modules that are used by the autograder.

If this is your first time working with Python's package system, you can read
more about it [here](https://docs.python.org/3/tutorial/modules.html#packages).

In essence, when you import `utils`, you really import the `__init__.py` file
which is meant to initialize the package. In this case, it imports all the
helpful functions from the other modules so that you can use them as if they
were all in the same file.

Look in the `__init__.py` to see which functions are exposed
externally and which modules those functions came from. 
Each function's documentation is with its definition. 

## Stdout checking

------------------------
For checking the presence of phrases in the student's output 

Simple checking example:

This does not take order into account 

```Python
expected_phrases = ["Welcome to my program", "Enter a value:",
                    "That number is even!", "Goodbye"]
for phrase in expected_phrases:
    if phrase not in student_output:
        raise AssertionError("Output is wrong!")
```

Based on the above example, the phrases could have been given in any order by 
the student, and it would still pass.
If instead you use `utils.phrases_out_of_order`,
it will not allow them to be out of order. 

Example using `utils.phrases_out_of_order`:

```Python
import utils 

expected_phrases = ["Welcome to my program", "Enter a value:",
                    "That number is even!", "Goodbye"]
missing_indexes = utils.phrases_out_of_order(expected_phrases, student_output)

if 0 in missing_indexes:
    print("Something is wrong with your welcome message")

if len(missing_indexes) > 0:
    raise AssertionError("Output is wrong!")
```

Once the first phrase is found ("Welcome to my program"), all the characters
that came before the first phrase are ignored when searching for the next 
phrase. 
This ensures that "Enter a value:" was printed at some point after 
"Welcome to my program" when the cases pass. 

You can also use `check_phrases` to have hints automatically made,
depending on
what hint level you use; however, this does give less control.