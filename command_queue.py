from queue import Queue
from threading import Thread
import logging

class CommandQueue:
    def __init__(self, router, worker_count=2):
        """
        Initializes the command queue.
        :param router: Instance of CommandRouter to process commands.
        :param worker_count: Number of worker threads to process commands.
        """
        self.queue = Queue()
        self.router = router
        self.workers = []
        self.worker_count = worker_count
        self.running = False

    def start(self):
        """Starts the worker threads."""
        self.running = True
        for i in range(self.worker_count):
            worker = Thread(target=self._process_queue, daemon=True, name=f"Worker-{i+1}")
            worker.start()
            self.workers.append(worker)
            logging.info(f"Started {worker.name}")

    def stop(self):
        """Stops the worker threads."""
        self.running = False
        # Put sentinel values to unblock threads
        for _ in self.workers:
            self.queue.put(None)
        for worker in self.workers:
            worker.join()
            logging.info(f"Stopped {worker.name}")

    def enqueue_command(self, command_string):
        """Enqueues a command for processing."""
        self.queue.put(command_string)
        logging.info(f"Enqueued command: {command_string}")

    def _process_queue(self):
        """Worker thread to process commands."""
        while self.running:
            command = self.queue.get()
            if command is None:
                # Sentinel value to exit
                break
            logging.info(f"{Thread.current_thread().name} processing command: {command}")
            response = self.router.route_command(command)
            self.handle_response(response)
            self.queue.task_done()

    def handle_response(self, response):
        """Handles the response from the router."""
        if isinstance(response, dict) and "error" in response:
            error = response["error"]
            print(f"Error {error['code']}: {error['message']}")
        else:
            print(response)
