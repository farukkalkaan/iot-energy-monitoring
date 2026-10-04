# IoT Energy Monitoring System

This project simulates an IoT energy monitoring device using real-world energy consumption data.

The system reads voltage, current and active power values from a real-world energy dataset, publishes the telemetry using MQTT, receives the data through an MQTT subscriber, and stores the measurements persistently in a PostgreSQL database.

## Architecture

Real-world energy dataset  
→ Python device simulator  
→ MQTT  
→ Mosquitto Broker  
→ MQTT consumer  
→ PostgreSQL database

## Technologies

- Python
- MQTT
- Mosquitto
- PostgreSQL
- paho-mqtt
- psycopg2
- python-dotenv

## Dataset

The project uses the UCI Individual Household Electric Power Consumption dataset.

The following measurements are used:

- Voltage: volts (V)
- Current: amperes (A)
- Active power: converted from kilowatts to watts (W)

The selected dataset does not contain temperature measurements. Therefore, temperature is represented by a constant 30 °C placeholder for demonstration purposes.

## MQTT

MQTT was selected because it is a lightweight publish/subscribe communication protocol commonly used in IoT systems.

MQTT topic:

```text
factory/motor1/telemetry
```
## Example MQTT Message
{
  "voltage": 234.84,
  "current": 18.4,
  "power": 4216.0,
  "temperature": 30.0
}
## Database Schema
CREATE TABLE telemetry (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    voltage_v DOUBLE PRECISION NOT NULL,
    current_a DOUBLE PRECISION NOT NULL,
    power_w DOUBLE PRECISION NOT NULL,
    temperature_c DOUBLE PRECISION NOT NULL
);
## Installation
Install the required Python packages:

python -m pip install -r requirements.txt

Make sure PostgreSQL and Mosquitto MQTT Broker are installed and running.
## Environment Variables
Create a .env file in the project directory:

DB_PASSWORD=your_postgresql_password
## Running the Project
Start the device simulator:

python device_simulator.py

Start the MQTT consumer in another terminal:

python mqtt_consumer.py
## Example Query
SELECT * FROM telemetry
ORDER BY id DESC;
## Security
Database credentials are not stored directly in the source code.
The PostgreSQL password is loaded from a local .env file using python-dotenv.
