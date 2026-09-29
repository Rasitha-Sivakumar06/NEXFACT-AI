import csv
from collections import defaultdict


# ============================================================
# AI FACTORY ENERGY COPILOT
# CONNECTED IMPACT ANALYSIS
# ============================================================

CSV_FILE = "factory_data.csv"

ELECTRICITY_COST_PER_KWH = 8.0
CO2_KG_PER_KWH = 0.70


# ============================================================
# PRODUCTION ORDERS
# ============================================================

orders = [
    {
        "order_id": "ORD001",
        "quantity": 500
    },
    {
        "order_id": "ORD002",
        "quantity": 700
    },
    {
        "order_id": "ORD003",
        "quantity": 400
    }
]


# ============================================================
# MACHINE CAPACITY
# ============================================================

machine_capacity = {
    "M01": 300,
    "M02": 250,
    "M03": 350
}


# ============================================================
# READ FACTORY DATA
# ============================================================

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


# ============================================================
# MACHINE HEALTH ANALYSIS
# ============================================================

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

    machine_health[machine_id] = health


# ============================================================
# ENERGY INTENSITY
# ============================================================

energy_per_unit = {}

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

    energy_per_unit[machine_id] = (
        total_energy / total_production
    )


# ============================================================
# FIND AI RECOMMENDATION
# ============================================================

def get_recommended_machine(quantity):

    candidates = []

    for machine_id in machine_capacity:

        health = machine_health.get(
            machine_id,
            "UNKNOWN"
        )

        energy = energy_per_unit.get(
            machine_id
        )

        if health == "HIGH_RISK":
            continue

        if energy is None:
            continue

        capacity = machine_capacity[machine_id]

        production_hours = (
            quantity / capacity
        )

        estimated_energy = (
            quantity * energy
        )

        candidates.append({
            "machine": machine_id,
            "health": health,
            "energy": energy,
            "hours": production_hours,
            "estimated_energy": estimated_energy
        })

    if not candidates:
        return None

    return min(
        candidates,
        key=lambda machine:
        machine["energy"]
    )


# ============================================================
# CALCULATE TOTAL IMPACT
# ============================================================

total_quantity = sum(
    order["quantity"]
    for order in orders
)


# ------------------------------------------------------------
# BASELINE
# ------------------------------------------------------------

# Baseline represents operation using the most
# energy-efficient machine without considering health.

baseline_machine = min(
    energy_per_unit,
    key=energy_per_unit.get
)


baseline_energy = (
    total_quantity
    * energy_per_unit[baseline_machine]
)


# ------------------------------------------------------------
# AI OPTIMIZED PLAN
# ------------------------------------------------------------

optimized_energy = 0

recommendations = []


for order in orders:

    recommendation = get_recommended_machine(
        order["quantity"]
    )

    if recommendation is None:
        continue

    recommendations.append({
        "order_id": order["order_id"],
        "machine": recommendation["machine"],
        "quantity": order["quantity"],
        "energy": recommendation["estimated_energy"]
    })

    optimized_energy += (
        recommendation["estimated_energy"]
    )


# ============================================================
# IMPACT CALCULATION
# ============================================================

energy_saved = (
    baseline_energy
    - optimized_energy
)


if baseline_energy > 0:

    savings_percentage = (
        energy_saved
        / baseline_energy
    ) * 100

else:

    savings_percentage = 0


baseline_cost = (
    baseline_energy
    * ELECTRICITY_COST_PER_KWH
)


optimized_cost = (
    optimized_energy
    * ELECTRICITY_COST_PER_KWH
)


cost_difference = (
    baseline_cost
    - optimized_cost
)


baseline_co2 = (
    baseline_energy
    * CO2_KG_PER_KWH
)


optimized_co2 = (
    optimized_energy
    * CO2_KG_PER_KWH
)


co2_reduction = (
    baseline_co2
    - optimized_co2
)


# ============================================================
# DISPLAY
# ============================================================

print("\n" + "=" * 85)
print("AI FACTORY ENERGY COPILOT")
print("CONNECTED ENERGY & IMPACT ANALYSIS")
print("=" * 85)


print("\nMACHINE HEALTH")
print("-" * 85)

for machine_id in machine_capacity:

    print(
        f"{machine_id} → "
        f"{machine_health.get(machine_id, 'UNKNOWN')}"
    )


print("\nBASELINE")
print("-" * 85)

print(
    f"Baseline machine: "
    f"{baseline_machine}"
)

print(
    f"Baseline energy: "
    f"{baseline_energy:.4f} kWh"
)


print("\nAI OPTIMIZED PRODUCTION PLAN")
print("-" * 85)


for recommendation in recommendations:

    print(
        f"{recommendation['order_id']} → "
        f"{recommendation['machine']} | "
        f"{recommendation['quantity']} units | "
        f"{recommendation['energy']:.4f} kWh"
    )


print("\n" + "=" * 85)
print("IMPACT")
print("=" * 85)


print(
    f"Baseline energy:     "
    f"{baseline_energy:.4f} kWh"
)

print(
    f"Optimized energy:    "
    f"{optimized_energy:.4f} kWh"
)

print(
    f"Energy difference:   "
    f"{energy_saved:.4f} kWh"
)

print(
    f"Energy change:       "
    f"{savings_percentage:.2f}%"
)

print(
    f"Baseline cost:       "
    f"₹{baseline_cost:.2f}"
)

print(
    f"Optimized cost:      "
    f"₹{optimized_cost:.2f}"
)

print(
    f"Cost difference:     "
    f"₹{cost_difference:.2f}"
)

print(
    f"Baseline CO2:        "
    f"{baseline_co2:.4f} kg"
)

print(
    f"Optimized CO2:       "
    f"{optimized_co2:.4f} kg"
)

print(
    f"Estimated CO2 change: "
    f"{co2_reduction:.4f} kg"
)


print("\n" + "=" * 85)
print("IMPACT ANALYSIS COMPLETE")
print("=" * 85)