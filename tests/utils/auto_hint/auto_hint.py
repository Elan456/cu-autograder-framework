from typing import List
from .hint_element import HintElement, HintSource
import json


class AutoHint:
    def __init__(
        self,
        target_url: str,
        project_directions_path: str = None,
        sample_output_path: str = None,
        class_id: str = None,
        project_id: str = None,
    ):
        self._target_url = target_url
        self._project_directions_path = project_directions_path
        self._sample_output_path = sample_output_path
        self._class_id = class_id
        self._project_id = project_id

        self._hint_elements: List[HintElement] = []

    def gen_hint(self):
        """
        Sends all the hint elements to the AutoHint API and
        returns the response
        """

        # Convert all hint elements to dictionaries
        hint_elements = [
            hint_element.to_dict() for hint_element in self._hint_elements
        ]

        # Covert to a json string
        hint_elements_json = json.dumps(hint_elements, indent=4)
        return hint_elements_json

    def reset(self):
        self._hint_elements = []

    def add_hint_element(self, hint_element: HintElement):
        self._hint_elements.append(hint_element)

    def add_sample_output(self, sample_output: str, **kwargs):
        self.add_hint_element(
            HintElement(sample_output, HintSource.SAMPLE_CODE, **kwargs)
        )

    def add_file(self, file_path: str, context: str, **kwargs):
        with open(file_path, "r") as f:
            self.add_hint_element(
                HintElement(f.read(), HintSource.INPUT_FILE, context, **kwargs)
            )

    def add_compile_error_message(self, error_message: str, **kwargs):
        self.add_hint_element(
            HintElement(error_message, HintSource.ERROR_MESSAGE, **kwargs)
        )

    def add_missing_phrase(self, phrase: str, **kwargs):
        self.add_hint_element(
            HintElement(phrase, HintSource.MISSING_PHRASE, **kwargs)
        )

    def add_function_signature(self, function_signature: str, **kwargs):
        self.add_hint_element(
            HintElement(
                function_signature, HintSource.FUNCTION_SIGNATURE, **kwargs
            )
        )

    def add_student_code_file(self, file_path: str, **kwargs):
        with open(file_path, "r") as f:
            self.add_hint_element(
                HintElement(f.read(), HintSource.STUDENT_CODE, **kwargs)
            )

    def add_timed_out(self, **kwargs):
        self.add_hint_element(HintElement("", HintSource.TIMED_OUT, **kwargs))
