import time
import logging
from threading import Thread

class AdapterHealthCheck:
    def __init__(self, interval=60):  # Check every minute
        self.interval = interval
        self.status = {}
        self.adapters = {}
        self.running = False

    def start_monitoring(self, adapters):
        """
        Starts the health monitoring in a separate thread.
        """
        self.adapters = adapters
        self.running = True
        self.worker = Thread(target=self._monitor_loop, daemon=True)
        self.worker.start()
        logging.info("Adapter health monitoring started.")

    def stop_monitoring(self):
        """
        Stops the health monitoring.
        """
        self.running = False
        logging.info("Adapter health monitoring stopped.")

    def _monitor_loop(self):
        while self.running:
            for name, adapter in self.adapters.items():
                try:
                    health = adapter.health_check()
                    self.status[name] = health
                    logging.info(f"Health Check - {name}: {health}")
                except Exception as e:
                    self.status[name] = {"status": "error", "error": str(e)}
                    logging.error(f"Health Check - {name}: Error during health check: {e}")
            time.sleep(self.interval)
