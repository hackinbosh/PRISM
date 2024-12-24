class Middleware:
    def process(self, command):
        """
        Process the command and return the modified command.
        This method should be overridden by all middleware implementations.
        """
        raise NotImplementedError("Middleware must implement the process method.")
