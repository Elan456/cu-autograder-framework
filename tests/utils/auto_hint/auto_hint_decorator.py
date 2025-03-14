"""
Add this decorator to the top of a testing function to utilize the patched
functions from auto_hint_patching.py
Will also enable you to access the AutoHint object in the function
"""

# auto_hint_decorator.py

import functools
from .auto_hint_patching import (
    patch_utils,
    unpatch_utils,
    set_current_hinter,
    get_current_hinter,
)
from utils.auto_hint import AutoHint


def autohint(test_func):
    """
    Decorator to monkey-patch the utils library, run the test,
    then unpatch afterward. Only the decorated test sees the patch.
    """

    @functools.wraps(test_func)
    def wrapper(*args, **kwargs):
        # Create or fetch your global AutoHinter instance.
        # Alternatively, you can create a new AutoHinter each time.
        if not get_current_hinter():
            ah = AutoHint("http://someHintServer")
            set_current_hinter(ah)

        # Apply the patch
        patch_utils()
        try:
            # Call the actual test function with the ah object
            args = (get_current_hinter(),) + args
            return test_func(*args, **kwargs)
        finally:
            # Unpatch so we restore normal behavior for other tests
            unpatch_utils()
            set_current_hinter(None)

    return wrapper
