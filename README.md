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