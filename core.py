import json
from importlib import import_module
import logging
from commands import Action
from errors import Error, ErrorCode
from command_schemas import get_validator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("prism.log"),
        logging.StreamHandler()
    ]
)

class CommandRouter:
    def __init__(self, adapter_config_path):
        self.adapters = self._load_adapters(adapter_config_path)
        self.middleware = []

    def add_middleware(self, middleware):
        """Adds a middleware to the middleware chain."""
        self.middleware.append(middleware)
        logging.info(f"Added middleware: {middleware.__class__.__name__}")

    def _execute_middleware_chain(self, command):
        """Executes the middleware chain on the command."""
        for middleware in self.middleware:
            command = middleware.process(command)
        return command

    def _load_adapters(self, config_path):
        """Loads adapter modules based on the configuration file."""
        adapters = {}
        with open(config_path, 'r') as f:
            config = json.load(f)
            for target, adapter_info in config.items():
                module_name = adapter_info.get("module")
                params = adapter_info.get("params", {})
                try:
                    module = import_module(f'adapters.{module_name}')
                    class_name = ''.join(word.capitalize() for word in module_name.split('_'))
                    adapter_class = getattr(module, class_name)
                    adapters[target] = adapter_class(**params)
                    logging.info(f"Loaded adapter for target '{target}': {module_name} with params {params}")
                except ImportError as e:
                    error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"ImportError: {e}")
                    logging.error(error.to_dict())
                except AttributeError:
                    error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"Class '{class_name}' not found in module '{module_name}'.")
                    logging.error(error.to_dict())
                except TypeError as e:
                    error = Error(ErrorCode.ADAPTER_INITIALIZATION_FAILED, f"TypeError: {e}")
                    logging.error(error.to_dict())
        return adapters

    def _validate_command_schema(self, command):
        """
        Validates the command against its schema.
        Returns an object with is_valid and errors attributes.
        """
        validator = get_validator(command)
        if not validator:
            return ValidatorResult(False, ["No schema defined for this command."])
        errors = sorted(validator.iter_errors(command), key=lambda e: e.path)
        if errors:
            error_messages = [error.message for error in errors]
            return ValidatorResult(False, error_messages)
        return ValidatorResult(True, [])

    def route_command(self, command_string):
        """Routes the command to the appropriate adapter."""
        try:
            command = json.loads(command_string)
            # Add schema validation
            validation_result = self._validate_command_schema(command)
            if not validation_result.is_valid:
                return Error(ErrorCode.INVALID_COMMAND, "; ".join(validation_result.errors)).to_dict()

            # Execute middleware chain
            command = self._execute_middleware_chain(command)

            action = command.get("action")
            target = command.get("target")

            # Validate action
            try:
                action_enum = Action(action)
            except ValueError:
                error = Error(ErrorCode.UNKNOWN_ACTION, f"Invalid action: {action}")
                logging.warning(error.to_dict())
                return error.to_dict()

            adapter = self.adapters.get(target)
            if adapter:
                logging.info(f"Routing command to adapter '{target}': {command}")
                result = adapter.execute(command)
                if isinstance(result, Error):
                    # Adapter returned an Error instance
                    standardized_error = Error(
                        code=result.code,
                        message=result.message
                    )
                    logging.error(standardized_error.to_dict())
                    return standardized_error.to_dict()
                else:
                    logging.info(f"Adapter response: {result}")
                    return result
            else:
                error = Error(ErrorCode.UNKNOWN_TARGET, f"No adapter found for target: {target}")
                logging.warning(error.to_dict())
                return error.to_dict()

        except json.JSONDecodeError:
            error = Error(ErrorCode.INVALID_COMMAND, "Invalid JSON command")
            logging.error(error.to_dict())
            return error.to_dict()
        except Exception as e:
            error = Error(ErrorCode.INTERNAL_ERROR, f"An unexpected error occurred: {e}")
            logging.exception(error.to_dict())
            return error.to_dict()

    def cleanup_all(self):
        """Cleans up all adapters that have a cleanup method."""
        for target, adapter in self.adapters.items():
            if hasattr(adapter, 'cleanup') and callable(adapter.cleanup):
                try:
                    adapter.cleanup()
                    logging.info(f"Cleaned up adapter '{target}'.")
                except Exception as e:
                    error = Error(ErrorCode.ADAPTER_EXECUTION_FAILED, f"Error during cleanup of adapter '{target}': {e}")
                    logging.error(error.to_dict())

class ValidatorResult:
    def __init__(self, is_valid, errors):
        self.is_valid = is_valid
        self.errors = errors
