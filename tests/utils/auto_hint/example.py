from utils.auto_hint import AutoHint
import utils
import os

# Run in the tests directory with the following command:
# python -m utils.auto_hint.example

USER = os.getenv("USER")


def test_01_intro_output():
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
        raise AssertionError(
            "The following phrases are missing or out of order:\n "
            + "\n".join([expected_phrases[i] for i in out_of_order])
        )


ah = AutoHint(
    "https://autohintingwebsite.com",
    project_directions_path="path/to/directions",
)


def test_01_intro_output_auto_hint():
    """Intro output is correct"""

    ah.reset()

    # Adding the relevant files to the auto hinter
    ah.add_student_code_file("../example_sample_code/studentMain.cpp")
    ah.add_student_code_file("../example_sample_code/studentFuncs.cpp")
    ah.add_student_code_file("../example_sample_code/studentFuncs.h")

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
        ah.add_compile_error_message(
            errors
        )  # Update auto hinter with the error message
        raise AssertionError(ah.gen_hint())  # Return the generated hint

    run = utils.run_program("example.out", txt_contents="1\n2\n1\n", user=USER)

    if run.timed_out:
        ah.add_timed_out()

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
        print("ooo")
        # Add all the missing phrases to the auto hint
        [ah.add_missing_phrase(expected_phrases[i]) for i in out_of_order]
        raise AssertionError(ah.gen_hint())


if __name__ == "__main__":
    try:
        test_01_intro_output()
    except AssertionError as e:
        print(e)

    try:
        test_01_intro_output_auto_hint()
    except AssertionError as e:
        print(e)
    print("All tests passed!")
