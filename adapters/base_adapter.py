import logging
from errors import Error, ErrorCode

class BaseAdapter:
    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit the runtime context and perform cleanup."""
        try:
            self.cleanup()
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during cleanup: {e}")
            logging.error(error.to_dict())
