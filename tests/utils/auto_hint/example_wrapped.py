from utils.auto_hint import AutoHint
from .auto_hint_decorator import autohint
import utils
import os

# Run in the tests directory with the following command:
# python -m utils.auto_hint.example

USER = os.getenv("USER")


@autohint
def test_automatic_auto_hinter(ah: AutoHint):
    """Intro output is correct"""

    _, errors = utils.subprocess_run(
        [
            "g++",
            "../example_sample_code/studentMain.cpp",
            "../example_sample_code/studentFuncs.cpp",
            "-I",
            "../example_sample_code/",
            "-o",
            "example.out",
        ],
        user=USER,
    )

    if errors:
        raise AssertionError(errors)
    run = utils.run_program("example.out", txt_contents="1\n2\n1\n", user=USER)

    # Checking for certain phrases in the output
    expected_phrases = [
        "Welcome to the calculators program!",
        "No input file given",
        "Defaulting to manual input",
    ]
    # Getting which phrases are missing or out-of-order
    # Returns the indexes of the phrases not found
    out_of_order = utils.phrases_out_of_order(expected_phrases, run.output)

    # If a phrase is missing, then you can give a helpful error message
    if len(out_of_order) > 0:
        hint = ah.gen_hint("Their output is missing at least one phrase.")
        raise AssertionError(hint)


if __name__ == "__main__":
    try:
        test_automatic_auto_hinter()
    except AssertionError as e:
        print(e)
