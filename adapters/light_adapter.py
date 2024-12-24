import logging
import requests
from errors import Error, ErrorCode
from adapters.base_adapter import BaseAdapter

class LightAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        self.api_endpoint = kwargs.get('api_endpoint', 'http://localhost:5000/api/lights/living_room')
        try:
            # Test API endpoint connectivity
            response = requests.get(self.api_endpoint)
            response.raise_for_status()
            logging.info(f"LightAdapter initialized with API endpoint: {self.api_endpoint}")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"Failed to initialize LightAdapter: {e}")
            logging.error(error.to_dict())
            raise e  # Let CommandRouter handle the error

    def execute(self, command):
        action = command.get("action")
        property = command.get("property")
        value = command.get("value")

        if action == "ACTUATE" and property == "state":
            try:
                # Implement light actuation logic here, e.g., sending a POST request to the API
                payload = {"state": value}
                response = requests.post(self.api_endpoint, json=payload)
                response.raise_for_status()
                logging.info(f"Light state set to: {value}")
                return {"status": f"Light set to {value}"}
            except Exception as e:
                error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error actuating light: {e}")
                logging.error(error.to_dict())
                return error
        else:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, "Unsupported action or property for LightAdapter")
            logging.warning(error.to_dict())
            return error

    def cleanup(self):
        try:
            # Implement any necessary cleanup logic here
            logging.info("LightAdapter cleanup completed.")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during cleanup: {e}")
            logging.error(error.to_dict())
