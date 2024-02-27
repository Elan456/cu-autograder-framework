"""
This file contains helpful functions for checking large stdout from the
student's code against expected output.

Some of these functions will help with sequential order and giving
helpful error messages without giving away the answers.
"""

import copy


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


class Phrase:
    """
    A class to store information about a phrase that was expected to be found
    """

    def __init__(self, phrase: str, loc: int):
        self.expected = phrase
        self.found = False
        self.loc = loc

        # The part of the mother_string that should have contained this
        # It's the section between the two closest expected phrases that
        # were found
        # Only exists if the phrase was not found
        self.probable_part = ""


def phrases_out_of_order_hint(
    expected_phrases: list[str], mother_string: str
) -> list[Phrase]:
    """
    Checking for each of these expected_phrases to be found within the
    mother_string. When a phrase is found, all the characters prior to it on
    the mother_string are ignored for future searches. As a result,
    if the first expected phrase is found at the end of the mother_string only,
    then there is no chance that the other phrases will be found.
    :returns    A list of Phrase objects that were not found
    """

    phrases = [Phrase(p, -1) for p in expected_phrases if len(p) > 0]

    # Step 1 -- Try to find each phrase such that one cannot be found at an
    # earlier index than the previous phrases

    cropped_string = copy.deepcopy(mother_string)
    for i, phrase in enumerate(phrases):
        loc = cropped_string.find(phrase.expected)
        if loc != -1:
            phrase.loc = len(mother_string) - len(cropped_string) + loc
            phrase.found = True
            cropped_string = cropped_string[loc + len(phrase.expected) :]

    # Step 2 -- For the ones that were not found, find the part of the
    # mother_string that should have contained it
    for i, phrase in enumerate(phrases):
        if not phrase.found:
            left_found = None
            right_found = None
            for j in range(i - 1, -1, -1):
                if phrases[j].found:
                    left_found = j
                    break
            for j in range(i + 1, len(phrases)):
                if phrases[j].found:
                    right_found = j
                    break

            if left_found is not None and right_found is not None:
                phrase.probable_part = mother_string[
                    phrases[left_found].loc
                    + len(phrases[left_found].expected) : phrases[
                        right_found
                    ].loc
                ]
            elif left_found is not None:
                phrase.probable_part = mother_string[
                    phrases[left_found].loc
                    + len(phrases[left_found].expected) :
                ]
            elif right_found is not None:
                phrase.probable_part = mother_string[
                    : phrases[right_found].loc
                ]
            else:
                phrase.probable_part = mother_string

    return [p for p in phrases if not p.found]


def check_phrases(
    expected_phrases: list[str], mother_string: str, hint_level=1
) -> str:
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

    missed_phrases = phrases_out_of_order_hint(expected_phrases, mother_string)

    # Everything was found
    if len(missed_phrases) == 0:
        return ""

    msg = "Fail\n\n"
    if hint_level >= 1:
        msg += missing_phrases_msg(len(missed_phrases), len(expected_phrases))
        msg += "\n\n"
    if hint_level >= 2:
        msg += "The following sections of your output did not contain an "
        msg += "expected phrase and are likely the cause for the issue:\n"
        used_probable_parts = []
        for i, p in enumerate(missed_phrases):
            if len(missed_phrases) > 0:
                pp = missed_phrases[i].probable_part
                if pp not in used_probable_parts:
                    used_probable_parts.append(pp)
                    msg += (
                        f"\n=========Sec {len(used_probable_parts)}=========\n"
                    )
                    msg += pp
                    msg += (
                        f"\n=======End Sec {len(used_probable_parts)}=======\n"
                    )
    if hint_level >= 3:
        msg += "\n\nHere are the expected phrases that were not found:\n"
        for i, p in enumerate(missed_phrases):
            msg += f"\n=========Phrase {i}=========\n" + p.expected
            msg += f"\n=======End Phrase {i}=======\n"

    return msg


def missing_phrases_msg(num_missing: int, num_expected: int) -> str:
    output = f"{num_missing} out of the {num_expected} phrases weren't found. "
    output += "Reference the sample output and double check the directions."
    return output
