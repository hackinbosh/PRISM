# PRISM

## Platform for Real-world Integration and Sensor Management

### Vision
PRISM is a modular framework designed to integrate and manage diverse sensors and actuators in real-world environments, providing seamless control and monitoring capabilities.

### Features
- **Sensor Integration:** Connect and manage various sensors effortlessly.
- **Actuation Control:** Execute commands to actuate devices in real-time.
- **Middleware Support:** Enhance functionality with customizable middleware.
- **Health Monitoring:** Continuously monitors the health of all integrated components.
- **Command Queue:** Handles high-load scenarios by queuing and processing commands efficiently.
- **Logging:** Comprehensive logging for tracking commands, middleware actions, adapter responses, and health checks.
- **Unit Testing:** Ensures reliability and correctness of core functionalities.

### Setup

#### Prerequisites
- Python 3.7+
- [Git](https://git-scm.com/downloads)
- [RPi.GPIO](https://pypi.org/project/RPi.GPIO/) (for Raspberry Pi GPIO control) *[Excluded on Windows]*
- [smbus2](https://pypi.org/project/smbus2/) (for I2C communication)
- [requests](https://pypi.org/project/requests/) (for HTTP requests)
- [jsonschema](https://pypi.org/project/jsonschema/) (for command validation)
- Any necessary hardware (e.g., Raspberry Pi, PIR sensor, smart light)

#### Installation
1. **Clone the Repository:**
    `ash
    git clone https://github.com/hackinbosh/PRISM.git
    cd PRISM
    `

2. **Install Dependencies:**
    `ash
    pip install -r requirements.txt
    `

3. **Configure Adapters:**
    - Open dapters_config.json.
    - Add mappings for your devices and corresponding adapters, including any required parameters.

4. **Run Example Script:**
    `ash
    python example.py
    `

### Usage
- **Define Commands:** Create JSON commands to observe or actuate devices.
- **Create Adapters:** Implement new adapters in the dapters/ directory following existing examples and leveraging the ase_adapter.py for context management.
- **Add Middleware:** Implement middleware by extending the Middleware class and add them to the CommandRouter.
- **Monitor Health:** Use the health monitoring system to keep track of adapter statuses.
- **Handle High Load:** Utilize the command queue to manage and process commands efficiently under high-load conditions.

### Adapter Development Guide
See [Adapter Development Guide](./AdapterDevelopmentGuide.md) for detailed instructions on adding new adapters.

### Contributing
- **Fork the Repository**
- **Create a Feature Branch**
- **Submit a Pull Request**

### License
[MIT](LICENSE)
