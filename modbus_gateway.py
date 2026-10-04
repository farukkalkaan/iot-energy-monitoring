import json
import time

import paho.mqtt.client as mqtt
from pymodbus.client import ModbusTcpClient

MODBUS_HOST = "127.0.0.1"
MODBUS_PORT = 5020

MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "factory/motor1/telemetry"

modbus_client = ModbusTcpClient(
    MODBUS_HOST,
    port=MODBUS_PORT
)

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
mqtt_client.loop_start()

if not modbus_client.connect():
    raise ConnectionError("Could not connect to Modbus device.")

print("Modbus gateway started.")

try:
    while True:
        response = modbus_client.read_holding_registers(
            address=0,
            count=4,
            slave=1
        )

        if response.isError():
            print("Modbus read error.")
            time.sleep(2)
            continue

        voltage_raw, current_raw, power_raw, temperature_raw = response.registers

        data = {
            "voltage": voltage_raw / 10,
            "current": current_raw / 100,
            "power": float(power_raw),
            "temperature": temperature_raw / 10,
        }

        mqtt_client.publish(
            MQTT_TOPIC,
            json.dumps(data)
        )

        print(
            f"Gateway -> MQTT | "
            f"Voltage: {data['voltage']} V | "
            f"Current: {data['current']} A | "
            f"Power: {data['power']} W | "
            f"Temperature: {data['temperature']} °C"
        )

        time.sleep(2)

finally:
    modbus_client.close()
    mqtt_client.loop_stop()