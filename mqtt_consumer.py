import os
import json
import psycopg2
import paho.mqtt.client as mqtt
from dotenv import load_dotenv

load_dotenv()

BROKER = "localhost"
PORT = 1883
TOPIC = "factory/motor1/telemetry"

DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "iot_energy"
DB_USER = "postgres"
DB_PASSWORD = os.getenv("DB_PASSWORD")


connection = psycopg2.connect(
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = connection.cursor()


def on_message(client, userdata, msg):

    message = msg.payload.decode()

    data = json.loads(message)

    print(
     f"Received -> Voltage: {data['voltage']} V | "
     f"Current: {data['current']} A | "
     f"Power: {data['power']} W | "
     f"Temperature: {data['temperature']} °C"
)

    cursor.execute(
    """
    INSERT INTO telemetry
    (voltage_v, current_a, power_w, temperature_c)
    VALUES (%s, %s, %s, %s)
    """,
    (
        data["voltage"],
        data["current"],
        data["power"],
        data["temperature"]
    )
)

    connection.commit()

    print("Saved to PostgreSQL.")


client = mqtt.Client()

client.on_message = on_message

client.connect(BROKER, PORT)

client.subscribe(TOPIC)

print("MQTT consumer started.")

client.loop_forever()