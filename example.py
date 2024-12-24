import json
import time
from core import CommandRouter
from errors import Error  # Ensure Error is imported
from middleware.logging_middleware import LoggingMiddleware
from health_monitor import AdapterHealthCheck
from command_queue import CommandQueue

# Initialize the Command Router with the adapters configuration
router = CommandRouter('adapters_config.json')

# Add Middleware
logging_middleware = LoggingMiddleware()
router.add_middleware(logging_middleware)

# Initialize Health Monitoring
health_monitor = AdapterHealthCheck(interval=60)  # Check every 60 seconds
health_monitor.start_monitoring(router.adapters)

# Initialize Command Queue
command_queue = CommandQueue(router, worker_count=3)
command_queue.start()

# Register cleanup function to be called on exit
import atexit
atexit.register(lambda: [command_queue.stop(), health_monitor.stop_monitoring(), router.cleanup_all()])

# Define commands
read_motion_command = json.dumps({
    "action": "OBSERVE",
    "target": "motion_sensor_1",
    "property": "motion_detected"
})

actuate_light_on_command = json.dumps({
    "action": "ACTUATE",
    "target": "living_room_light",
    "property": "state",
    "value": "ON"
})

actuate_light_off_command = json.dumps({
    "action": "ACTUATE",
    "target": "living_room_light",
    "property": "state",
    "value": "OFF"
})

read_temp_command = json.dumps({
    "action": "OBSERVE",
    "target": "temperature_sensor_1",
    "property": "current_temperature"
})

read_humidity_command = json.dumps({
    "action": "OBSERVE",
    "target": "humidity_sensor_1",
    "property": "current_humidity"
})

# Enqueue commands for processing
commands = [
    read_motion_command,
    read_temp_command,
    read_humidity_command,
    actuate_light_on_command,
    actuate_light_off_command
]

for cmd in commands:
    command_queue.enqueue_command(cmd)

# Optionally, keep the main thread alive to continue processing
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down gracefully.")
finally:
    command_queue.stop()
    health_monitor.stop_monitoring()
    router.cleanup_all()
