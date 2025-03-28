import enum


class HintSource(enum.Enum):
    ERROR_MESSAGE = 0
    STUDENT_CODE = 1
    SAMPLE_CODE = 2
    FUNCTION_SIGNATURE = 3
    TEST_CASE_NAME = 4
    INPUT_FILE = 5
    TEST_USER_INPUT = 15  # User input for the test cases
    SAMPLE_OUTPUT = 6
    PROJECT_DIRECTIONS = 7
    PROJECT_DESCRIPTION = 8
    MISSING_PHRASE = 9
    EXPECTED_PHRASE = 14
    TIMED_OUT = 10
    STUDENT_OUTPUT = 11
    GENERAL = 12
    TEST_CASE = 13
    SHELL_COMMAND = 16
    COMPILE_STEP = 17
    FILE = 18
    FINAL_CONTEXT = 19


class HintElement:
    def __init__(
        self,
        content: str,
        source: HintSource,
        context: str = "",
        relevance: float = 1.0,
        metadata: dict = {},
    ):
        self.content = content
        self.source = source
        self.context = context
        self.relevance = relevance
        self.metadata = metadata

    def to_dict(self):
        d = {
            "content": self.content,
            "source": self.source.name,
            "context": self.context,
            "relevance": self.relevance,
            "metadata": self.metadata,
        }

        # Make the dict json safe
        return {k: v for k, v in d.items() if v is not None}

    @staticmethod
    def from_dict(data: dict):
        return HintElement(
            data["content"],
            HintSource[data["source"]],
            data["context"],
            data["relevance"],
            data["metadata"],
        )
