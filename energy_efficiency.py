import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"


# --------------------------------------------------
# READ FACTORY DATA
# --------------------------------------------------

machine_data = defaultdict(list)

with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]

        machine_data[machine_id].append({
            "state": row["state"],
            "power": float(row["power_kw"]),
            "production": int(row["production_units"])
        })


# --------------------------------------------------
# CALCULATE ENERGY EFFICIENCY
# --------------------------------------------------

print("\n" + "=" * 80)
print("AI FACTORY ENERGY COPILOT")
print("OBSERVED ENERGY EFFICIENCY ANALYSIS")
print("=" * 80)


efficiency_results = {}


for machine_id, readings in machine_data.items():

    # Only use productive operating states
    productive_readings = [
        reading
        for reading in readings
        if reading["production"] > 0
        and reading["state"] != "ABNORMAL"
    ]

    if not productive_readings:
        continue


    total_power = sum(
        reading["power"]
        for reading in productive_readings
    )

    total_production = sum(
        reading["production"]
        for reading in productive_readings
    )


    # --------------------------------------------------
    # Observed energy intensity
    #
    # Since each reading represents approximately
    # one 2-second interval:
    #
    # Energy = Power × Time
    # --------------------------------------------------

    interval_hours = 2 / 3600

    total_energy_kwh = (
        total_power * interval_hours
    )


    energy_per_unit = (
        total_energy_kwh / total_production
    )


    efficiency_results[machine_id] = {
        "energy": total_energy_kwh,
        "production": total_production,
        "energy_per_unit": energy_per_unit
    }


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

for machine_id, result in efficiency_results.items():

    print(f"\nMachine: {machine_id}")

    print(
        f"Total observed energy : "
        f"{result['energy']:.4f} kWh"
    )

    print(
        f"Total production      : "
        f"{result['production']} units"
    )

    print(
        f"Energy per unit       : "
        f"{result['energy_per_unit']:.6f} kWh/unit"
    )


# --------------------------------------------------
# COMPARE MACHINES
# --------------------------------------------------

if efficiency_results:

    most_efficient = min(
        efficiency_results.items(),
        key=lambda item: item[1]["energy_per_unit"]
    )


    print("\n" + "=" * 80)
    print("ENERGY EFFICIENCY COMPARISON")
    print("=" * 80)


    for machine_id, result in sorted(
        efficiency_results.items(),
        key=lambda item: item[1]["energy_per_unit"]
    ):

        print(
            f"{machine_id} → "
            f"{result['energy_per_unit']:.6f} kWh/unit"
        )


    print("\nMost energy-efficient observed machine:")

    print(
        f"  {most_efficient[0]} "
        f"({most_efficient[1]['energy_per_unit']:.6f} kWh/unit)"
    )


print("\n" + "=" * 80)
print("ENERGY EFFICIENCY ANALYSIS COMPLETE")
print("=" * 80)