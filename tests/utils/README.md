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



