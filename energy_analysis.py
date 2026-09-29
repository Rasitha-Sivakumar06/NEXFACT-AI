import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"

# Simulator generates one reading every 2 seconds.
# Therefore, each power reading represents approximately 2 seconds.
INTERVAL_SECONDS = 2


def calculate_energy(power_kw):
    """
    Calculate energy consumed during one interval.

    Energy (kWh) = Power (kW) × Time (hours)
    """
    time_hours = INTERVAL_SECONDS / 3600
    return power_kw * time_hours


machine_data = defaultdict(lambda: {
    "total_energy_kwh": 0,
    "total_production": 0,
    "readings": 0
})


with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]

        power_kw = float(row["power_kw"])
        production_units = int(row["production_units"])

        energy_kwh = calculate_energy(power_kw)

        machine_data[machine_id]["total_energy_kwh"] += energy_kwh
        machine_data[machine_id]["total_production"] += production_units
        machine_data[machine_id]["readings"] += 1


print("\n" + "=" * 70)
print("AI FACTORY ENERGY COPILOT - ENERGY ANALYSIS")
print("=" * 70)


for machine_id, data in machine_data.items():

    total_energy = data["total_energy_kwh"]
    total_production = data["total_production"]

    if total_production > 0:
        sec = total_energy / total_production
    else:
        sec = 0

    print(f"\nMachine: {machine_id}")
    print(f"Readings: {data['readings']}")
    print(f"Total Energy: {total_energy:.4f} kWh")
    print(f"Total Production: {total_production} units")
    print(f"SEC: {sec:.6f} kWh/unit")


print("\n" + "=" * 70)