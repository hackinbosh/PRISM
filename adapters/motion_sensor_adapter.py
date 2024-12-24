import logging
import sys
from errors import Error, ErrorCode
from adapters.base_adapter import BaseAdapter

try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except ImportError:
    GPIO_AVAILABLE = False
    logging.warning("RPi.GPIO not available. GPIO functionalities will be disabled.")

class MotionSensorAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        self.pin = kwargs.get('pin', 17)  # Default GPIO pin if not provided
        if GPIO_AVAILABLE:
            try:
                GPIO.setmode(GPIO.BCM)
                GPIO.setup(self.pin, GPIO.IN)
                logging.info(f"MotionSensorAdapter initialized on GPIO pin {self.pin}")
            except Exception as e:
                error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"Failed to initialize MotionSensorAdapter: {e}")
                logging.error(error.to_dict())
                raise e  # Let CommandRouter handle the error
        else:
            logging.info("GPIO not available. MotionSensorAdapter initialized without GPIO.")

    def execute(self, command):
        action = command.get("action")
        property = command.get("property")

        if action == "OBSERVE" and property == "motion_detected":
            if GPIO_AVAILABLE:
                try:
                    motion = GPIO.input(self.pin)
                    logging.info(f"Motion detected: {'Yes' if motion else 'No'}")
                    return {"motion_detected": bool(motion)}
                except Exception as e:
                    error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error reading motion sensor: {e}")
                    logging.error(error.to_dict())
                    return error
            else:
                # Simulate motion detection for development purposes
                logging.info("GPIO not available. Simulating motion detection.")
                return {"motion_detected": False}
        else:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, "Unsupported action or property for MotionSensorAdapter")
            logging.warning(error.to_dict())
            return error

    def cleanup(self):
        try:
            if GPIO_AVAILABLE:
                GPIO.cleanup()
                logging.info("GPIO cleanup completed for MotionSensorAdapter")
            else:
                logging.info("No GPIO cleanup needed for MotionSensorAdapter")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during GPIO cleanup: {e}")
            logging.error(error.to_dict())
