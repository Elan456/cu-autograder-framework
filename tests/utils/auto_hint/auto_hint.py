from typing import List
from .hint_element import HintElement, HintSource
import json
import requests
import datetime


"""
Example CURL to autohinter server:

curl -X POST "18.116.43.74:8081/generate_hint" \
     -H "Content-Type: application/json" \
     -d '{
           "hint_elements": [{
             "content": "Welcome to the calculators program!",
             "source": "SAMPLE_CODE",
             "context": "intro output",
             "relevance": 1.0,
             "metadata": null
            }],
           "use_knowledge_base": true,
           "temperature": 0.2,
           "top_p": 0.7,
           "max_tokens": 1024,
           "top_k": 4,
           "collection_name": "nvidia_blogs",
           "model": "meta/llama-3.1-70b-instruct",
           "stop": []
         }'


curl -X POST "http://localhost:8081/generate_hint" \
     -H "Content-Type: application/json" \
     -d '{"hint_elements": [{"content": "Welcome to the calculators program!",
     "source": "MISSING_PHRASE",
     "context": "", "relevance": 1.0,
     "metadata": {}}],
     "use_knowledge_base": false,
     "temperature": 0.2,
     "top_p": 0.7,
     "max_tokens": 1024,
     "top_k": 4,
     "collection_name": "nvidia_blogs",
     "model": "meta/llama-3.1-70b-instruct",
     "stop": []}'

The response is a series of fastapi StreamingResponse
"""


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

    def gen_hint(self):
        """
        Sends all the hint elements to the AutoHint API and
        returns the response
        """

        # Convert all hint elements to dictionaries
        hint_elements = [
            hint_element.to_dict() for hint_element in self._hint_elements
        ]

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
