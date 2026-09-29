import csv
from collections import defaultdict


# ============================================================
# AI FACTORY ENERGY COPILOT
# UNIFIED FACTORY DECISION ENGINE
# ============================================================

CSV_FILE = "factory_data.csv"

ELECTRICITY_COST_PER_KWH = 8.0
CO2_KG_PER_KWH = 0.70


# ============================================================
# MACHINE CONFIGURATION
# ============================================================

machines = {
    "M01": {
        "capacity_per_hour": 300,
        "available_hours": 4
    },

    "M02": {
        "capacity_per_hour": 250,
        "available_hours": 4
    },

    "M03": {
        "capacity_per_hour": 350,
        "available_hours": 4
    }
}


# ============================================================
# PRODUCTION ORDERS
# ============================================================

orders = [
    {
        "order_id": "ORD001",
        "product": "Component-A",
        "quantity": 500,
        "deadline_hours": 4,
        "priority": "HIGH"
    },

    {
        "order_id": "ORD002",
        "product": "Component-B",
        "quantity": 700,
        "deadline_hours": 5,
        "priority": "MEDIUM"
    },

    {
        "order_id": "ORD003",
        "product": "Component-C",
        "quantity": 400,
        "deadline_hours": 6,
        "priority": "LOW"
    }
]


# ============================================================
# LOAD FACTORY DATA
# ============================================================

machine_data = defaultdict(list)

with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]

        machine_data[machine_id].append({
            "timestamp": row["timestamp"],
            "state": row["state"],
            "power": float(row["power_kw"]),
            "temperature": float(row["temperature_c"]),
            "vibration": float(row["vibration_mm_s"]),
            "rpm": float(row["rpm"]),
            "production": int(row["production_units"]),
            "status": row["status"]
        })


# ============================================================
# PHASE 1 — MACHINE HEALTH
# ============================================================

machine_health = {}

abnormal_events = {}

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

    abnormal_events[machine_id] = abnormal_count

    if abnormal_count > 0:

        machine_health[machine_id] = "HIGH_RISK"

    elif high_load_count > 0:

        machine_health[machine_id] = "MONITOR"

    else:

        machine_health[machine_id] = "NORMAL"


# ============================================================
# PHASE 2 — ENERGY EFFICIENCY
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
# PHASE 3 — PRODUCTION SCHEDULING
# ============================================================

priority_weight = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


machine_workload = {
    machine_id: 0
    for machine_id in machines
}


machine_energy = {
    machine_id: 0
    for machine_id in machines
}


schedule = []


# Process high-priority orders first.

sorted_orders = sorted(
    orders,
    key=lambda order:
    priority_weight[order["priority"]],
    reverse=True
)


for order in sorted_orders:

    candidates = []


    for machine_id in machines:

        health = machine_health.get(
            machine_id,
            "UNKNOWN"
        )


        # Never schedule a HIGH_RISK machine.

        if health == "HIGH_RISK":
            continue


        if machine_id not in energy_per_unit:
            continue


        capacity = machines[machine_id][
            "capacity_per_hour"
        ]


        production_time = (
            order["quantity"] / capacity
        )


        projected_workload = (
            machine_workload[machine_id]
            + production_time
        )


        available_hours = machines[machine_id][
            "available_hours"
        ]


        # Check machine availability.

        if projected_workload > available_hours:
            continue


        # Check order deadline.

        if production_time > order["deadline_hours"]:
            continue


        energy = (
            order["quantity"]
            * energy_per_unit[machine_id]
        )


        # ----------------------------------------------------
        # HEALTH SCORE
        # ----------------------------------------------------

        if health == "NORMAL":

            health_score = 100

        else:

            health_score = 60


        # ----------------------------------------------------
        # ENERGY SCORE
        # ----------------------------------------------------

        max_energy = max(
            energy_per_unit.values()
        )

        min_energy = min(
            energy_per_unit.values()
        )


        if max_energy == min_energy:

            energy_score = 100

        else:

            energy_score = (
                (max_energy - energy_per_unit[machine_id])
                /
                (max_energy - min_energy)
            ) * 100


        # ----------------------------------------------------
        # CAPACITY SCORE
        # ----------------------------------------------------

        max_capacity = max(
            machine["capacity_per_hour"]
            for machine in machines.values()
        )


        capacity_score = (
            capacity / max_capacity
        ) * 100


        # ----------------------------------------------------
        # WORKLOAD SCORE
        # ----------------------------------------------------

        workload_ratio = (
            projected_workload
            / available_hours
        )


        workload_score = (
            1 - workload_ratio
        ) * 100


        # ----------------------------------------------------
        # FINAL DECISION SCORE
        # ----------------------------------------------------

        final_score = (
            health_score * 0.40
            +
            energy_score * 0.30
            +
            capacity_score * 0.10
            +
            workload_score * 0.20
        )


        candidates.append({
            "machine": machine_id,
            "health": health,
            "production_time": production_time,
            "energy": energy,
            "score": final_score
        })


    if not candidates:
        continue


    selected = max(
        candidates,
        key=lambda candidate:
        candidate["score"]
    )


    machine_id = selected["machine"]


    machine_workload[machine_id] += (
        selected["production_time"]
    )


    machine_energy[machine_id] += (
        selected["energy"]
    )


    schedule.append({
        "order_id": order["order_id"],
        "product": order["product"],
        "quantity": order["quantity"],
        "priority": order["priority"],
        "machine": machine_id,
        "time": selected["production_time"],
        "energy": selected["energy"],
        "score": selected["score"]
    })


# ============================================================
# PHASE 4 — IMPACT ANALYSIS
# ============================================================

total_energy = sum(
    machine_energy.values()
)


total_production = sum(
    order["quantity"]
    for order in orders
)


energy_cost = (
    total_energy
    * ELECTRICITY_COST_PER_KWH
)


co2_emissions = (
    total_energy
    * CO2_KG_PER_KWH
)


machines_used = len([
    machine_id
    for machine_id, workload in machine_workload.items()
    if workload > 0
])


# ============================================================
# DASHBOARD OUTPUT
# ============================================================

print("\n")
print("=" * 100)
print("AI FACTORY ENERGY COPILOT")
print("UNIFIED FACTORY INTELLIGENCE ENGINE")
print("=" * 100)


# ============================================================
# FACTORY OVERVIEW
# ============================================================

print("\nFACTORY OVERVIEW")
print("-" * 100)

print(
    f"Machines monitored       : {len(machines)}"
)

print(
    f"Production orders        : {len(orders)}"
)

print(
    f"Total planned production : {total_production} units"
)

print(
    f"Machines utilized        : {machines_used}"
)


# ============================================================
# MACHINE HEALTH
# ============================================================

print("\nMACHINE HEALTH")
print("-" * 100)


for machine_id in machines:

    print(
        f"{machine_id} | "
        f"Health: {machine_health[machine_id]} | "
        f"Abnormal events: {abnormal_events[machine_id]} | "
        f"Energy/unit: "
        f"{energy_per_unit.get(machine_id, 0):.6f} kWh"
    )


# ============================================================
# PRODUCTION DECISIONS
# ============================================================

print("\nAI PRODUCTION DECISIONS")
print("-" * 100)


for item in schedule:

    print(
        f"{item['order_id']} → {item['machine']} | "
        f"{item['quantity']} units | "
        f"{item['priority']} | "
        f"{item['time']:.2f} h | "
        f"{item['energy']:.4f} kWh | "
        f"Score {item['score']:.2f}"
    )


# ============================================================
# MACHINE UTILIZATION
# ============================================================

print("\nMACHINE UTILIZATION")
print("-" * 100)


for machine_id in machines:

    available_hours = machines[machine_id][
        "available_hours"
    ]

    workload = machine_workload[machine_id]

    utilization = (
        workload
        / available_hours
    ) * 100


    print(
        f"{machine_id} | "
        f"Workload: {workload:.2f} h | "
        f"Utilization: {utilization:.1f}% | "
        f"Health: {machine_health[machine_id]}"
    )


# ============================================================
# ENERGY IMPACT
# ============================================================

print("\nENERGY IMPACT")
print("-" * 100)

print(
    f"Estimated production energy : "
    f"{total_energy:.4f} kWh"
)

print(
    f"Estimated electricity cost   : "
    f"₹{energy_cost:.2f}"
)

print(
    f"Estimated CO2 emissions      : "
    f"{co2_emissions:.4f} kg"
)


# ============================================================
# SAFETY DECISION
# ============================================================

print("\nSAFETY DECISIONS")
print("-" * 100)


high_risk = [
    machine_id
    for machine_id in machines
    if machine_health[machine_id] == "HIGH_RISK"
]


if high_risk:

    for machine_id in high_risk:

        print(
            f"⚠️ {machine_id} excluded from production "
            f"because of HIGH_RISK condition."
        )

else:

    print(
        "No high-risk machines detected."
    )


# ============================================================
# COPILOT SUMMARY
# ============================================================

print("\nCOPILOT SUMMARY")
print("-" * 100)


print(
    "✓ Factory data analyzed"
)

print(
    "✓ Machine health evaluated"
)

print(
    "✓ Abnormal conditions detected"
)

print(
    "✓ Energy efficiency calculated"
)

print(
    "✓ High-risk machines excluded"
)

print(
    "✓ Production orders scheduled"
)

print(
    "✓ Energy impact estimated"
)

print(
    "✓ Operating cost estimated"
)

print(
    "✓ CO2 impact estimated"
)


print("\n" + "=" * 100)
print("AI FACTORY ENERGY COPILOT — ANALYSIS COMPLETE")
print("=" * 100)