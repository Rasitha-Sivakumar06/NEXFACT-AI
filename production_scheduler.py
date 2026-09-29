import csv
from collections import defaultdict


# ============================================================
# AI FACTORY ENERGY COPILOT
# PRODUCTION SCHEDULER
# ============================================================

CSV_FILE = "factory_data.csv"


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
# MACHINE HEALTH
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
# ORDER PRIORITY
# ============================================================

priority_weight = {
    "HIGH": 3,
    "MEDIUM": 2,
    "LOW": 1
}


# ============================================================
# MACHINE STATUS
# ============================================================

print("\n" + "=" * 95)
print("AI FACTORY ENERGY COPILOT")
print("PRODUCTION SCHEDULER")
print("=" * 95)

print("\nMACHINE STATUS")
print("-" * 95)

for machine_id in machines:

    print(
        f"{machine_id} | "
        f"Health: {machine_health.get(machine_id, 'UNKNOWN')} | "
        f"Capacity: {machines[machine_id]['capacity_per_hour']} units/hour | "
        f"Available: {machines[machine_id]['available_hours']} hours"
    )


# ============================================================
# TRACK MACHINE WORKLOAD
# ============================================================

machine_workload = {
    machine_id: 0
    for machine_id in machines
}


machine_energy = {
    machine_id: 0
    for machine_id in machines
}


schedule = []


# ============================================================
# SORT ORDERS BY PRIORITY
# ============================================================

sorted_orders = sorted(
    orders,
    key=lambda order:
    priority_weight[order["priority"]],
    reverse=True
)


# ============================================================
# SCHEDULE ORDERS
# ============================================================

for order in sorted_orders:

    candidates = []


    for machine_id in machines:

        health = machine_health.get(
            machine_id,
            "UNKNOWN"
        )

        # Never assign production to a high-risk machine.

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


        current_workload = (
            machine_workload[machine_id]
        )


        projected_workload = (
            current_workload
            + production_time
        )


        available_hours = machines[machine_id][
            "available_hours"
        ]


        # Machine cannot accept this order
        # if its workload exceeds availability.

        if projected_workload > available_hours:
            continue


        # Check individual order deadline.

        if production_time > order["deadline_hours"]:
            continue


        energy = (
            order["quantity"]
            * energy_per_unit[machine_id]
        )


        # ----------------------------------------------------
        # MACHINE SCORE
        # ----------------------------------------------------

        if health == "NORMAL":
            health_score = 100
        else:
            health_score = 60


        max_capacity = max(
            machine["capacity_per_hour"]
            for machine in machines.values()
        )


        capacity_score = (
            capacity / max_capacity
        ) * 100


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


        # Prefer machines with lower existing workload.

        workload_ratio = (
            projected_workload
            /
            available_hours
        )


        workload_score = (
            1 - workload_ratio
        ) * 100


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
            "final_score": final_score
        })


    # ========================================================
    # SELECT MACHINE
    # ========================================================

    if not candidates:

        print(
            f"\n⚠️ {order['order_id']} "
            f"could not be scheduled."
        )

        continue


    selected = max(
        candidates,
        key=lambda candidate:
        candidate["final_score"]
    )


    machine_id = selected["machine"]


    # Update machine workload.

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
        "production_time": selected["production_time"],
        "energy": selected["energy"],
        "score": selected["final_score"]
    })


# ============================================================
# DISPLAY FINAL SCHEDULE
# ============================================================

print("\n" + "=" * 95)
print("FINAL PRODUCTION SCHEDULE")
print("=" * 95)


for item in schedule:

    print(
        f"\n{item['order_id']} → "
        f"{item['machine']}"
    )

    print(
        f"Product: {item['product']}"
    )

    print(
        f"Quantity: {item['quantity']} units"
    )

    print(
        f"Priority: {item['priority']}"
    )

    print(
        f"Production time: "
        f"{item['production_time']:.2f} hours"
    )

    print(
        f"Estimated energy: "
        f"{item['energy']:.4f} kWh"
    )

    print(
        f"Decision score: "
        f"{item['score']:.2f}/100"
    )


# ============================================================
# MACHINE UTILIZATION
# ============================================================

print("\n" + "=" * 95)
print("MACHINE UTILIZATION")
print("=" * 95)


for machine_id in machines:

    available_hours = machines[machine_id][
        "available_hours"
    ]

    workload = machine_workload[machine_id]

    utilization = (
        workload / available_hours
    ) * 100


    print(
        f"{machine_id} | "
        f"Workload: {workload:.2f} h | "
        f"Available: {available_hours:.2f} h | "
        f"Utilization: {utilization:.1f}% | "
        f"Health: {machine_health[machine_id]}"
    )


# ============================================================
# TOTAL ENERGY
# ============================================================

total_energy = sum(
    machine_energy.values()
)


print("\n" + "=" * 95)
print("ENERGY SUMMARY")
print("=" * 95)

print(
    f"Estimated total production energy: "
    f"{total_energy:.4f} kWh"
)


# ============================================================
# SAFETY SUMMARY
# ============================================================

high_risk_machines = [
    machine_id
    for machine_id in machines
    if machine_health[machine_id] == "HIGH_RISK"
]


print("\n" + "=" * 95)
print("SAFETY SUMMARY")
print("=" * 95)


if high_risk_machines:

    print(
        "High-risk machines excluded from scheduling:"
    )

    for machine_id in high_risk_machines:

        print(
            f"  ⚠️ {machine_id}"
        )

else:

    print(
        "No high-risk machines detected."
    )


print("\n" + "=" * 95)
print("PRODUCTION SCHEDULING COMPLETE")
print("=" * 95)