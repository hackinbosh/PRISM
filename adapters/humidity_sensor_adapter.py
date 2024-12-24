import logging
import smbus2
import time
from errors import Error, ErrorCode
from adapters.base_adapter import BaseAdapter

class HumiditySensorAdapter(BaseAdapter):
    def __init__(self, **kwargs):
        self.bus = kwargs.get('bus', 1)
        self.address = int(kwargs.get('address', '0x40'), 16)
        try:
            self.bus = smbus2.SMBus(self.bus)
            logging.info(f"HumiditySensorAdapter initialized on I2C bus {self.bus} at address {hex(self.address)}")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"Failed to initialize HumiditySensorAdapter: {e}")
            logging.error(error.to_dict())
            raise e

    def execute(self, command):
        action = command.get("action")
        property = command.get("property")

        if action == "OBSERVE" and property == "current_humidity":
            try:
                self.bus.write_byte(self.address, 0xF5)
                time.sleep(0.5)
                data = self.bus.read_i2c_block_data(self.address, 0x00, 2)
                humidity = ((data[0] << 8) | data[1]) * 125.0 / 65536.0 - 6.0
                logging.info(f"Read humidity: {humidity}%")
                return {"current_humidity": humidity}
            except Exception as e:
                error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error reading humidity sensor: {e}")
                logging.error(error.to_dict())
                return error
        else:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, "Unsupported action or property for HumiditySensorAdapter")
            logging.warning(error.to_dict())
            return error

    def cleanup(self):
        try:
            self.bus.close()
            logging.info("I2C bus closed for HumiditySensorAdapter")
        except Exception as e:
            error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during I2C bus cleanup: {e}")
            logging.error(error.to_dict())
