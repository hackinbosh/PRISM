import logging
from middleware import Middleware

class LoggingMiddleware(Middleware):
    def process(self, command):
        logging.info(f"Middleware Logging: Processing command: {command}")
        return command  # Return the command unmodified
