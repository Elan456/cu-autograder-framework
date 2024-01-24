"""
This file contains helpful functions for checking large stdout from the
student's code against expected output.

Some of these functions will help with sequential order and giving
helpful error messages without giving away the answers.
"""


def phrases_out_of_order(expected_phrases, mother_string) -> list:
    """
    Checks if a list of phrases appear in a larger string in the correct order
    Ignores extra characters between phrases. Use `check_phrase` if you want
    built-in error messages and hints.

    expected_phrases : list of substrings to search for in output
    mother_string : string that could contain all of the expected_phrases

    returns the indexes of the phrases not found
    """
    not_found = []
    for i, phrase in enumerate(expected_phrases):
        # Getting the first location of the string
        loc = mother_string.find(phrase)
        if loc == -1:
            not_found.append(i)
        else:
            # Removing the phrase and everything before it
            mother_string = mother_string[loc + len(phrase) :]
    return not_found


def phrases_out_of_order_hint(expected_phrases, mother_string):
    """
    Checking for each of these expected_phrases to be found within the
    mother_string. When a phrase is found, all the characters prior to it on
    the mother_string are ignored for future searches. As a result,
    if the first expected phrase is found at the end of the mother_string only,
    then there is no chance that the other phrases will be found.
    :returns    The list of phrases indexes that were missing and
                a list of strings that likely should contain the missing
                phrases.
                These two lists are parallel, so the first index of the
                not_found list will correspond to the first index of the
                parts_skipped list
    """
    not_found = []  # Index of the phrases that were not found
    parts_skipped = (
        []
    )  # Parallel to the not_found list, indicates what parts were skipped

    waiting_for_skip = 0
    for i, phrase in enumerate(expected_phrases):
        # Getting the first location of the string
        loc = mother_string.find(phrase)
        if loc == -1:
            not_found.append(i)
            waiting_for_skip += 1
        else:
            # If somethings werent found, append the most
            # recent parts skipped because that is where the
            # phrase was expected to be an is likely where the error
            # is
            if waiting_for_skip > 0:
                parts_skipped.extend(["" for _ in range(waiting_for_skip - 1)])
                parts_skipped.append(mother_string[:loc])
                waiting_for_skip = 0
            # Removing the phrase and everything before it
            mother_string = mother_string[loc + len(phrase) :]
    # If when you get to the end, there are still not_found phrases waiting
    # for their skip info to be used as a hint, give whatever is left in the
    # mother_string
    if waiting_for_skip > 0:
        parts_skipped.extend(["" for _ in range(waiting_for_skip - 1)])
        parts_skipped.append(mother_string)
    return not_found, parts_skipped


def check_phrases(expected_phrases, mother_string, hint_level=1) -> str:
    """
    Checks if all the expected phrases are in the output in the correct order

    :param expected_phrases A list of the phrases that should be in the
                            mother_string in the correct order

    :param mother_string    The string that is expected to contain all the
                            expected_phrases (usually the student's output)

    :param hint_level       How much of a hint should be given in the error
                            message
                            0 = Only the word "fail" will be returned if
                                something isn't found
                            1 = Will tell the number of phrases that were
                                missing out of how many were expected
                            2 = Will output the parts of the mother_string
                                that should have contained a phrase. Good for
                                helping them find typos in a large output.
                                WARNING - could reveal what the testcases do
                            3 = Will output the info from 2 along with what the
                                expected_phrases are
                                WARNING - will reveal what the testcase is
                                checking for exactly

    :returns                An empty string if all the expected_phrases are
                            found, and an error message otherwise.
                            This error message should be raised as an
                            AssertionError in your unit testing script if
                            it's not empty
    """

    not_found, part_skipped = phrases_out_of_order_hint(
        expected_phrases, mother_string
    )

    # Everything was found
    if len(not_found) == 0:
        return ""

    msg = "Fail... "
    if hint_level >= 1:
        msg += missing_phrases_msg(len(not_found), len(expected_phrases))
        msg += "\n\n"
    if hint_level >= 2:
        msg += "The following sections of your output did not contain an "
        msg += "expected phrase and are likely the cause for the issue:\n"
        for p in part_skipped:
            if len(p) > 0:
                msg += "\n====================\n" + p
        msg += "\n====================\n"
    if hint_level >= 3:
        msg += "\n\nHere are the expected phrases that were not found:\n"
        for i in not_found:
            msg += "\n-----\n" + expected_phrases[i]
        msg += "\n-----\n"

    return msg


def missing_phrases_msg(num_missing: int, num_expected: int) -> str:
    output = f"{num_missing} out of the {num_expected} phrases weren't found. "
    output += "Make sure you check over the sample output "
    output += "to match all the specific phrases that are being used."
    return output
