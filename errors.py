from enum import Enum

class ErrorCode(Enum):
    INVALID_COMMAND = 1001
    UNKNOWN_ACTION = 1002
    UNKNOWN_TARGET = 1003
    ADAPTER_INITIALIZATION_FAILED = 1004
    ADAPTER_EXECUTION_FAILED = 1005
    INTERNAL_ERROR = 1006

class Error:
    def __init__(self, code: ErrorCode, message: str):
        self.code = code
        self.message = message

    def to_dict(self):
        return {
            "error": {
                "code": self.code.value,
                "message": self.message
            }
        }
