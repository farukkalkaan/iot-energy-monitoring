import asyncio
import pandas as pd

from pymodbus.server import StartAsyncTcpServer
from pymodbus.datastore import (
    ModbusSequentialDataBlock,
    ModbusSlaveContext,
    ModbusServerContext,
)

CSV_FILE = "household_power_consumption.txt"


def load_dataset():
    df = pd.read_csv(
        CSV_FILE,
        sep=";",
        na_values="?",
        usecols=[
            "Global_active_power",
            "Voltage",
            "Global_intensity",
        ],
    )

    return df.dropna().reset_index(drop=True)


async def update_registers(context, df):
    index = 0

    while True:
        row = df.iloc[index % len(df)]

        voltage = int(row["Voltage"] * 10)
        current = int(row["Global_intensity"] * 100)
        power = int(row["Global_active_power"] * 1000)
        temperature = 300

        registers = [
            voltage,
            current,
            power,
            temperature,
        ]

        context[0].setValues(3, 0, registers)

        print(
            f"Modbus device -> "
            f"Voltage: {voltage / 10} V | "
            f"Current: {current / 100} A | "
            f"Power: {power} W | "
            f"Temperature: {temperature / 10} °C"
        )

        index += 1
        await asyncio.sleep(2)


async def main():
    df = load_dataset()

    store = ModbusSlaveContext(
        hr=ModbusSequentialDataBlock(0, [0] * 10)
    )

    context = ModbusServerContext(
        slaves=store,
        single=True
    )

    asyncio.create_task(update_registers(context, df))

    print("Modbus TCP device started on localhost:5020")

    await StartAsyncTcpServer(
        context=context,
        address=("127.0.0.1", 5020),
    )


if __name__ == "__main__":
    asyncio.run(main())