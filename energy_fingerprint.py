import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"


machine_data = defaultdict(list)


# -----------------------------------------
# READ FACTORY DATA
# -----------------------------------------

with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]
        state = row["state"]
        power = float(row["power_kw"])

        machine_data[machine_id].append({
            "state": state,
            "power": power
        })


print("\n" + "=" * 70)
print("AI FACTORY ENERGY COPILOT")
print("ENERGY FINGERPRINT ANALYSIS")
print("=" * 70)


# -----------------------------------------
# LEARN NORMAL ENERGY FINGERPRINT
# -----------------------------------------

fingerprints = {}


for machine_id, readings in machine_data.items():

    normal_power = []

    for reading in readings:

        if reading["state"] == "NORMAL":
            normal_power.append(reading["power"])

    if len(normal_power) == 0:
        continue

    average_power = sum(normal_power) / len(normal_power)

    minimum_power = min(normal_power)
    maximum_power = max(normal_power)

    fingerprints[machine_id] = {
        "average": average_power,
        "minimum": minimum_power,
        "maximum": maximum_power
    }


# -----------------------------------------
# DISPLAY ENERGY FINGERPRINT
# -----------------------------------------

print("\nNORMAL ENERGY FINGERPRINT")
print("-" * 70)


for machine_id, fingerprint in fingerprints.items():

    print(f"\nMachine: {machine_id}")

    print(
        f"Average Power : "
        f"{fingerprint['average']:.2f} kW"
    )

    print(
        f"Normal Range  : "
        f"{fingerprint['minimum']:.2f} - "
        f"{fingerprint['maximum']:.2f} kW"
    )


# -----------------------------------------
# CHECK ALL READINGS
# -----------------------------------------

print("\n" + "=" * 70)
print("ENERGY FINGERPRINT CHECK")
print("=" * 70)


for machine_id, readings in machine_data.items():

    if machine_id not in fingerprints:
        continue

    fingerprint = fingerprints[machine_id]

    minimum = fingerprint["minimum"]
    maximum = fingerprint["maximum"]

    print(f"\nMachine: {machine_id}")

    for reading in readings:

        power = reading["power"]
        state = reading["state"]

        # Only evaluate NORMAL-state readings
        # against the NORMAL fingerprint.
        if state != "NORMAL":
            continue

        if minimum <= power <= maximum:

            result = "NORMAL"

        else:

            result = "ANOMALY"

        print(
            f"Power: {power:.2f} kW | "
            f"State: {state:6} | "
            f"Result: {result}"
        )


print("\n" + "=" * 70)
