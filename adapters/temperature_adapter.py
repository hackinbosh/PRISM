import logging
from errors import Error, ErrorCode
from adapters.base_adapter import BaseAdapter

class TemperatureAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        self.port = kwargs.get('port', '/dev/ttyUSB0')  # Default port if not provided
        self.baudrate = kwargs.get('baudrate', 9600)    # Default baudrate if not provided
        try:
            # Initialize serial connection here, e.g.,
            # self.serial = serial.Serial(self.port, self.baudrate)
            logging.info(f"TemperatureAdapter initialized with port: {self.port}, baudrate: {self.baudrate}")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"Failed to initialize TemperatureAdapter: {e}")
            logging.error(error.to_dict())
            raise e  # Let CommandRouter handle the error

    def execute(self, command):
        action = command.get("action")
        property = command.get("property")

        if action == "OBSERVE" and property == "current_temperature":
            try:
                # Implement temperature reading logic here
                temperature = 25.0  # Placeholder value
                logging.info(f"Read temperature: {temperature}°C")
                return {"current_temperature": temperature}
            except Exception as e:
                error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error reading temperature: {e}")
                logging.error(error.to_dict())
                return error
        else:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, "Unsupported action or property for TemperatureAdapter")
            logging.warning(error.to_dict())
            return error

    def cleanup(self):
        try:
            # Implement cleanup logic here, e.g., closing serial connection
            # self.serial.close()
            logging.info("TemperatureAdapter cleanup completed.")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during cleanup: {e}")
            logging.error(error.to_dict())
