import logging
from errors import Error, ErrorCode
from adapters.base_adapter import BaseAdapter

class DummyAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        # Initialization logic
        logging.info("DummyAdapter initialized.")

    def execute(self, command):
        # Execution logic
        action = command.get("action")
        target = command.get("target")

        if action == "TEST" and target == "dummy_adapter":
            logging.info("Dummy action executed.")
            return {"status": "Dummy action executed successfully."}
        else:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, "Unsupported action or target for DummyAdapter")
            logging.warning(error.to_dict())
            return error

    def cleanup(self):
        try:
            # Cleanup logic
            logging.info("DummyAdapter cleanup completed.")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during cleanup: {e}")
            logging.error(error.to_dict())
