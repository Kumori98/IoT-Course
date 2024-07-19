# Arduino-based IoT Device Simulation with CherryPy and MQTT

This laboratory simulates an Internet of Things (IoT) device using an Arduino board, CherryPy as a web framework, and the MQTT message protocol for communication.

## Components

### Hardware

- Arduino board (e.g., Uno, Nano, etc.) with Wi-Fi or Ethernet capability (depending on your connection method)
- Sensors (temperature, light)

### Software

- Arduino IDE: [Download and install Arduino IDE](https://support.arduino.cc/hc/en-us/articles/360019833020-Download-and-install-Arduino-IDE)
- Python 3: [Download Python 3](https://www.python.org/downloads/)
- CherryPy web framework: Install via pip
- Paho MQTT library: Install via pip

## Setup

### Install Software

1. Download and install the Arduino IDE and Python 3.
2. Use pip to install CherryPy and Paho MQTT libraries.

### Prepare Arduino Code

Develop your Arduino code to:

- Read sensor data (if applicable)
- Connect to your MQTT broker 
- Publish sensor data or simulated values to a specific MQTT topic

### Develop CherryPy Web Application

Create a Python script using CherryPy to:

- Subscribe to the same MQTT topic used by the Arduino device
- Upon receiving data, process and potentially visualize it using a web interface
- Optionally, provide controls to interact with the simulated device (e.g., sending commands)

## Running the Project

### Upload Arduino Sketch

1. Open your Arduino code in the Arduino IDE.
2. Select your Arduino board and port.
3. Upload the sketch to your Arduino board.

### Start CherryPy Application

1. Open a terminal in the directory containing your CherryPy script.
2. Run the script using `python your_script.py`. This will start the web server.

### Access Web Interface

Open a web browser and navigate to `http://localhost:<port>`, where `<port>` is the port specified in your CherryPy script (default is usually 8080).

## Customization

- Modify the Arduino code to simulate different sensor data types or behaviors.
- Adapt the CherryPy application to handle the specific data format and visualization requirements of your simulation.
- Consider security measures if connecting your device to a public MQTT broker.

