from typing import List
from .hint_element import HintElement, HintSource
import json
import requests
import datetime
import inspect


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
        self._target_endpoint = f"{target_url}/generate_hint"
        self._project_directions_path = project_directions_path
        self._sample_output_path = sample_output_path
        self._class_id = class_id
        self._project_id = project_id

        self._hint_elements: List[HintElement] = []

    def gen_hint(self, context: str = None) -> str:
        """
        Sends all the hint elements to the AutoHint API and
        returns the response

        :param context: Optional context to be added to the hint elements
        :return: The generated hint as a string
        """

        if context:
            self.add_hint_element(
                HintElement(
                    context,
                    HintSource.FINAL_CONTEXT,
                    "Context given by the autograder developer right before"
                    " they call the hint generation",
                    relevance=1,
                )
            )

        # Convert all hint elements to dictionaries
        hint_elements = [
            hint_element.to_dict() for hint_element in self._hint_elements
        ]

        with open("hint_elements.json", "w") as f:
            json.dump(hint_elements, f, indent=4)

        # Build a request to the autohinter server
        request_data = {
            "hint_elements": hint_elements,
            "use_knowledge_base": False,
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "top_k": 4,
            "collection_name": "nvidia_blogs",
            "model": "meta/llama-3.1-70b-instruct",
            "stop": [],
        }

        log_path = "request_data" + str(datetime.datetime.now()) + ".json"
        # Write  the request data to a file
        with open(log_path, "w") as f:
            json.dump(request_data, f, indent=4)

        # print(self._hint_elements[0].to_dict())

        # Send the request to the autohinter server
        response = requests.post(self._target_endpoint, json=request_data)
        output = ""
        # Process the streaming response
        for line in response.iter_lines():
            if line:
                # Filter out the 'data: ' prefix and parse JSON
                if line.startswith(b"data: "):
                    json_str = line[6:].decode("utf-8")
                    try:
                        data = json.loads(json_str)
                        if "choices" in data and data["choices"]:
                            if (
                                "delta" in data["choices"][0]
                                and "content" in data["choices"][0]["delta"]
                            ):
                                content = data["choices"][0]["delta"][
                                    "content"
                                ]
                                if content:
                                    output += content
                    except json.JSONDecodeError:
                        print(f"Failed to parse: {json_str}")

        with open(log_path, "a") as f:
            f.write(output)

        return output

    def reset(self):
        self._hint_elements = []

    def add_test_case(self):
        """
        Captures the entire function body from which this method is called
        and stores it as a hint element.
        """
        frame = inspect.currentframe().f_back  # Get the caller's frame
        function_name = frame.f_code.co_name  # Get the function name

        try:
            # Retrieve the source code of the function
            source_lines, start_line = inspect.getsourcelines(frame)
            source_code = "".join(source_lines)

            # Store the function's code as a hint
            self.add_hint_element(
                HintElement(
                    content=function_name,
                    source=HintSource.TEST_CASE_NAME,
                    context="Name of the test case that failed",
                )
            )

            self.add_hint_element(
                HintElement(
                    content=source_code,
                    source=HintSource.TEST_CASE,
                    context="Code of the test case that failed",
                )
            )
        except Exception as e:
            print(f"Failed to retrieve source code: {e}")

    def add_hint_element(self, hint_element: HintElement):
        self._hint_elements.append(hint_element)

    def add_sample_output(self, sample_output: str, **kwargs):
        self.add_hint_element(
            HintElement(sample_output, HintSource.SAMPLE_CODE, **kwargs)
        )

    def add_student_output(self, student_output: str, **kwargs):
        self.add_hint_element(
            HintElement(student_output, HintSource.STUDENT_CODE, **kwargs)
        )

    def add_file(self, file_path: str, context: str, **kwargs):
        context += " from " + file_path
        metadata = kwargs.get("metadata", {})
        metadata["file_path"] = file_path
        with open(file_path, "r") as f:
            self.add_hint_element(
                HintElement(
                    f.read(),
                    HintSource.FILE,
                    context,
                    metadata=metadata,
                    **kwargs,
                )
            )

    def add_compile_error_message(self, error_message: str, **kwargs):
        self.add_hint_element(
            HintElement(error_message, HintSource.ERROR_MESSAGE, **kwargs)
        )

    def add_missing_phrase(self, phrase: str, **kwargs):
        self.add_hint_element(
            HintElement(phrase, HintSource.MISSING_PHRASE, **kwargs)
        )

    def add_expected_phrase(self, phrase: str, **kwargs):
        self.add_hint_element(
            HintElement(phrase, HintSource.EXPECTED_PHRASE, **kwargs)
        )

    def add_function_signature(self, function_signature: str, **kwargs):
        self.add_hint_element(
            HintElement(
                function_signature, HintSource.FUNCTION_SIGNATURE, **kwargs
            )
        )

    def add_student_code_file(self, file_path: str, **kwargs):
        with open(file_path, "r") as f:
            context = f"Students code from {file_path}"
            self.add_hint_element(
                HintElement(
                    f.read(),
                    HintSource.STUDENT_CODE,
                    context=context,
                    **kwargs,
                )
            )

    def add_timed_out(self, **kwargs):
        self.add_hint_element(HintElement("", HintSource.TIMED_OUT, **kwargs))

    def add_test_user_input(self, user_input: str, **kwargs):
        self.add_hint_element(
            HintElement(user_input, HintSource.TEST_USER_INPUT, **kwargs)
        )

    def add_shell_command(self, command: str, **kwargs):
        self.add_hint_element(
            HintElement(command, HintSource.SHELL_COMMAND, **kwargs)
        )
