# Tests Folder

- `test.py` - The main test file. It should contain Python unit tests.
- `utils` - Python package containing modules with helper functions for testing.
More info in the `utils/README.md` file.
- `drivers` - Everything placed in this folder will be copied into the source
directory before testing. This is useful for including drivers for testing
individual functions.

## Security

Everything in this folder cannot be read by the "student" user.
When the drivers are copied into the source directory, they are still owned
by the "root" user, so the "student" user cannot read them. To still use them, compile
the drivers as "root" and then run them as "student." You wouldn't be able to
compile them as "student" because they cannot read the drivers.


