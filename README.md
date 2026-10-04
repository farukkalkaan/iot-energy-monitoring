# IoT Energy Monitoring System

This project simulates an industrial IoT energy monitoring pipeline using real-world energy consumption data.

The system reads voltage, current and active power values from a real-world dataset, exposes them through a simulated Modbus TCP device, reads them through a Modbus gateway, publishes the telemetry using MQTT, and stores the measurements persistently in a PostgreSQL database.

## Architecture

UCI Energy Dataset  
→ Modbus TCP Device Simulator  
→ Modbus Gateway  
→ MQTT / Mosquitto Broker  
→ MQTT Consumer  
→ PostgreSQL Database

## Technologies

- Python
- Modbus TCP
- MQTT
- Mosquitto
- PostgreSQL
- paho-mqtt
- pymodbus
- psycopg2
- pandas
- python-dotenv

## Dataset

The project uses the UCI Individual Household Electric Power Consumption dataset.

The following measurements are used:

- Voltage: volts (V)
- Current: amperes (A)
- Active power: converted from kilowatts to watts (W)

The selected dataset does not contain temperature measurements. Therefore, temperature is represented by a constant 30 °C placeholder for demonstration purposes.

The dataset file should be placed in the project directory with the following filename:

household_power_consumption.txt

Dataset source:
UCI Individual Household Electric Power Consumption Dataset

## Protocols

### Modbus TCP

Modbus TCP is used to simulate device-level industrial communication.

The simulated Modbus device stores telemetry values in holding registers.

Register mapping:

- Register 0: Voltage × 10
- Register 1: Current × 100
- Register 2: Active power in watts
- Register 3: Temperature × 10

### MQTT

MQTT is used by the gateway to publish telemetry to the backend using a lightweight publish/subscribe architecture.

MQTT topic:

factory/motor1/telemetry

Example MQTT message:

{
  "voltage": 234.84,
  "current": 18.4,
  "power": 4216.0,
  "temperature": 30.0
}

## Database Schema

The telemetry data is stored in PostgreSQL.

The table structure is:

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

Make sure the following services are installed and running:

- Mosquitto MQTT Broker
- PostgreSQL

Create a PostgreSQL database named:

iot_energy

Then run the SQL schema contained in:

schema.sql

## Environment Variables

Create a `.env` file in the project directory:

DB_PASSWORD=your_postgresql_password

The `.env` file is excluded from Git using `.gitignore`.

## Running the Project

Run the components in the following order.

1. Start PostgreSQL.

2. Start the Modbus TCP device simulator:

python modbus_device.py

3. Start the Modbus gateway:

python modbus_gateway.py

4. Start the MQTT consumer:

python mqtt_consumer.py

The complete data flow is:

Dataset  
→ Modbus TCP Device  
→ Modbus Gateway  
→ MQTT  
→ Mosquitto Broker  
→ MQTT Consumer  
→ PostgreSQL

## Example Database Query

SELECT * FROM telemetry
ORDER BY id DESC;

## Project Structure

iot-energy-monitoring/
- modbus_device.py
- modbus_gateway.py
- mqtt_consumer.py
- device_simulator.py
- schema.sql
- requirements.txt
- .gitignore
- README.md

## Security

Database credentials are not stored directly in the source code.

The PostgreSQL password is loaded from a local `.env` file using python-dotenv.