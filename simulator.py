import random
import time
import csv
import os
from datetime import datetime


MACHINES = ["M01", "M02", "M03"]

CSV_FILE = "factory_data.csv"

FIELDNAMES = [
    "timestamp",
    "machine_id",
    "state",
    "power_kw",
    "temperature_c",
    "vibration_mm_s",
    "rpm",
    "production_units",
    "status"
]


machine_states = {
    "M01": {
        "state": "NORMAL",
        "counter": 0
    },
    "M02": {
        "state": "NORMAL",
        "counter": 0
    },
    "M03": {
        "state": "NORMAL",
        "counter": 0
    }
}


def create_csv_file():

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writeheader()


def change_machine_state(machine_id):

    machine = machine_states[machine_id]

    machine["counter"] += 1

    # M02 will experience a controlled anomaly
    if machine_id == "M02":

        if 20 <= machine["counter"] < 28:
            machine["state"] = "ABNORMAL"
            return

    # Normal state changes
    if machine["counter"] % 8 == 0:

        states = [
            "STARTUP",
            "NORMAL",
            "HIGH_LOAD",
            "NORMAL",
            "IDLE"
        ]

        machine["state"] = random.choice(states)


def generate_machine_data(machine_id):

    change_machine_state(machine_id)

    state = machine_states[machine_id]["state"]

    # -----------------------------------
    # ABNORMAL
    # -----------------------------------

    if state == "ABNORMAL":

        power = random.uniform(6.5, 7.5)
        temperature = random.uniform(55, 65)
        vibration = random.uniform(4.0, 6.0)
        rpm = random.randint(1200, 1350)
        production = random.randint(12, 20)

    # -----------------------------------
    # STARTUP
    # -----------------------------------

    elif state == "STARTUP":

        power = random.uniform(5.0, 6.0)
        temperature = random.uniform(35, 42)
        vibration = random.uniform(1.5, 2.5)
        rpm = random.randint(1000, 1300)
        production = random.randint(5, 10)

    # -----------------------------------
    # NORMAL
    # -----------------------------------

    elif state == "NORMAL":

        power = random.uniform(3.8, 4.8)
        temperature = random.uniform(38, 45)
        vibration = random.uniform(1.0, 2.0)
        rpm = random.randint(1400, 1500)
        production = random.randint(18, 30)

    # -----------------------------------
    # HIGH LOAD
    # -----------------------------------

    elif state == "HIGH_LOAD":

        power = random.uniform(5.0, 6.5)
        temperature = random.uniform(45, 55)
        vibration = random.uniform(2.0, 3.5)
        rpm = random.randint(1300, 1450)
        production = random.randint(25, 35)

    # -----------------------------------
    # IDLE
    # -----------------------------------

    else:

        power = random.uniform(0.5, 1.2)
        temperature = random.uniform(30, 36)
        vibration = random.uniform(0.3, 0.8)
        rpm = random.randint(0, 300)
        production = 0

    return {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "machine_id": machine_id,
        "state": state,
        "power_kw": round(power, 2),
        "temperature_c": round(temperature, 2),
        "vibration_mm_s": round(vibration, 2),
        "rpm": rpm,
        "production_units": production,
        "status": "RUNNING" if state != "IDLE" else "IDLE"
    }


def save_data(data):

    with open(CSV_FILE, "a", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=FIELDNAMES
        )

        writer.writerow(data)


# Start a fresh dataset
create_csv_file()


print("\nAI FACTORY ENERGY COPILOT")
print("CONTROLLED ANOMALY SIMULATOR")
print("=" * 80)


while True:

    print("\n" + "=" * 80)

    for machine in MACHINES:

        data = generate_machine_data(machine)

        save_data(data)

        print(
            f"{data['machine_id']} | "
            f"{data['state']:10} | "
            f"Power: {data['power_kw']:5} kW | "
            f"Temp: {data['temperature_c']:5} C | "
            f"Vibration: {data['vibration_mm_s']:4} | "
            f"RPM: {data['rpm']:4} | "
            f"Production: {data['production_units']:2}"
        )

    print("=" * 80)
    print("Data saved to factory_data.csv")
    print("Next reading in 2 seconds...")

    time.sleep(2)