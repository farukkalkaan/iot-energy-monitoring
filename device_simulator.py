import csv
import json
import time
import paho.mqtt.client as mqtt

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/motor1/telemetry"

client = mqtt.Client()
client.connect(BROKER, PORT)

print("IoT device simulator started.")

with open(
    "household_power_consumption.txt",
    "r",
    encoding="utf-8"
) as file:

    reader = csv.DictReader(file, delimiter=";")

    for row in reader:

        if "?" in row.values():
            continue

        voltage = float(row["Voltage"])
        current = float(row["Global_intensity"])

        power_kw = float(row["Global_active_power"])
        power_w = power_kw * 1000

        data = {
            "voltage": voltage,
            "current": current,
            "power": round(power_w, 2),
            "temperature": 30.0
        }

        message = json.dumps(data)

        client.publish(TOPIC, message)

        print(
           f"Sent -> Voltage: {voltage} V | "
           f"Current: {current} A | "
           f"Power: {round(power_w, 2)} W | "
           f"Temperature: 30.0 °C"
)

        time.sleep(2)