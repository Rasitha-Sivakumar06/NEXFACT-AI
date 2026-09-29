import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"


# ==================================================
# MACHINE CONFIGURATION
# ==================================================

machines = {
    "M01": {
        "capacity_per_hour": 300
    },

    "M02": {
        "capacity_per_hour": 250
    },

    "M03": {
        "capacity_per_hour": 350
    }
}


# ==================================================
# PRODUCTION ORDERS
# ==================================================

orders = [
    {
        "order_id": "ORD001",
        "product": "Component-A",
        "quantity": 500,
        "deadline": "14:00",
        "priority": "HIGH"
    },

    {
        "order_id": "ORD002",
        "product": "Component-B",
        "quantity": 700,
        "deadline": "16:00",
        "priority": "MEDIUM"
    },

    {
        "order_id": "ORD003",
        "product": "Component-C",
        "quantity": 400,
        "deadline": "18:00",
        "priority": "LOW"
    }
]


# ==================================================
# READ FACTORY DATA
# ==================================================

machine_data = defaultdict(list)

with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]

        machine_data[machine_id].append({
            "state": row["state"],
            "power": float(row["power_kw"]),
            "temperature": float(row["temperature_c"]),
            "vibration": float(row["vibration_mm_s"]),
            "production": int(row["production_units"])
        })


# ==================================================
# CALCULATE MACHINE HEALTH
# ==================================================

machine_health = {}

for machine_id, readings in machine_data.items():

    abnormal_count = sum(
        1
        for reading in readings
        if reading["state"] == "ABNORMAL"
    )

    high_load_count = sum(
        1
        for reading in readings
        if reading["state"] == "HIGH_LOAD"
    )

    if abnormal_count > 0:

        health = "HIGH_RISK"

    elif high_load_count > 0:

        health = "MONITOR"

    else:

        health = "NORMAL"


    machine_health[machine_id] = {
        "health": health,
        "abnormal_events": abnormal_count
    }


# ==================================================
# CALCULATE OBSERVED ENERGY INTENSITY
# ==================================================

energy_efficiency = {}


for machine_id, readings in machine_data.items():

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


    interval_hours = 2 / 3600


    total_energy = (
        total_power * interval_hours
    )


    energy_per_unit = (
        total_energy / total_production
    )


    energy_efficiency[machine_id] = energy_per_unit


# ==================================================
# DISPLAY MACHINE PROFILE
# ==================================================

print("\n" + "=" * 90)
print("AI FACTORY ENERGY COPILOT")
print("UNIFIED ENERGY-AWARE PRODUCTION OPTIMIZER")
print("=" * 90)


print("\nMACHINE PROFILE")
print("-" * 90)


for machine_id in machines:

    health = machine_health.get(
        machine_id,
        {}
    ).get(
        "health",
        "UNKNOWN"
    )


    energy = energy_efficiency.get(
        machine_id,
        0
    )


    capacity = machines[machine_id][
        "capacity_per_hour"
    ]


    print(
        f"{machine_id} | "
        f"Health: {health:10} | "
        f"Energy: {energy:.6f} kWh/unit | "
        f"Capacity: {capacity} units/hour"
    )


# ==================================================
# PRODUCTION OPTIMIZATION
# ==================================================

print("\n" + "=" * 90)
print("ENERGY-AWARE PRODUCTION DECISIONS")
print("=" * 90)


for order in orders:

    print(
        f"\nORDER: {order['order_id']}"
    )

    print(
        f"Product: {order['product']}"
    )

    print(
        f"Quantity: {order['quantity']} units"
    )

    print(
        f"Priority: {order['priority']}"
    )

    print(
        f"Deadline: {order['deadline']}"
    )

    print("-" * 90)


    candidates = []


    for machine_id in machines:

        health = machine_health.get(
            machine_id,
            {}
        ).get(
            "health",
            "UNKNOWN"
        )


        energy = energy_efficiency.get(
            machine_id
        )


        capacity = machines[machine_id][
            "capacity_per_hour"
        ]


        # ------------------------------------------
        # HIGH-RISK MACHINE
        # ------------------------------------------

        if health == "HIGH_RISK":

            print(
                f"{machine_id} → "
                f"AVOID | "
                f"Reason: HIGH-RISK MACHINE"
            )

            continue


        # ------------------------------------------
        # Missing efficiency data
        # ------------------------------------------

        if energy is None:

            print(
                f"{machine_id} → "
                f"NOT AVAILABLE | "
                f"Reason: insufficient data"
            )

            continue


        # ------------------------------------------
        # Production time
        # ------------------------------------------

        production_hours = (
            order["quantity"]
            / capacity
        )


        # ------------------------------------------
        # Estimated energy
        # ------------------------------------------

        estimated_energy = (
            order["quantity"]
            * energy
        )


        # ------------------------------------------
        # Candidate
        # ------------------------------------------

        candidates.append({
            "machine": machine_id,
            "health": health,
            "energy_per_unit": energy,
            "capacity": capacity,
            "hours": production_hours,
            "estimated_energy": estimated_energy
        })


        print(
            f"{machine_id} → "
            f"AVAILABLE | "
            f"{energy:.6f} kWh/unit | "
            f"{production_hours:.2f} hours | "
            f"{estimated_energy:.4f} kWh"
        )


    # ==================================================
    # SELECT RECOMMENDATION
    # ==================================================

    if not candidates:

        print(
            "\n⚠️ NO SUITABLE MACHINE AVAILABLE"
        )

        continue


    # Healthy machines are preferred.
    # Among them, select the lowest observed
    # energy consumption per unit.

    best_machine = min(
        candidates,
        key=lambda machine:
        machine["energy_per_unit"]
    )


    print("\n" + "-" * 90)

    print("RECOMMENDATION")

    print(
        f"Machine: "
        f"{best_machine['machine']}"
    )

    print(
        f"Health: "
        f"{best_machine['health']}"
    )

    print(
        f"Observed energy intensity: "
        f"{best_machine['energy_per_unit']:.6f} kWh/unit"
    )

    print(
        f"Estimated production time: "
        f"{best_machine['hours']:.2f} hours"
    )

    print(
        f"Estimated energy: "
        f"{best_machine['estimated_energy']:.4f} kWh"
    )

    print(
        "\nReason:"
    )

    print(
        "  ✓ Machine health acceptable"
    )

    print(
        "  ✓ Production capacity available"
    )

    print(
        "  ✓ Lower observed energy intensity "
        "among available machines"
    )


# ==================================================
# FINAL MESSAGE
# ==================================================

print("\n" + "=" * 90)
print("PRODUCTION OPTIMIZATION COMPLETE")
print("=" * 90)