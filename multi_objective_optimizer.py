import csv
from collections import defaultdict


# ============================================================
# AI FACTORY ENERGY COPILOT
# MULTI-OBJECTIVE PRODUCTION OPTIMIZER
# ============================================================

CSV_FILE = "factory_data.csv"


# ============================================================
# MACHINE CONFIGURATION
# ============================================================

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


# ============================================================
# PRODUCTION ORDERS
# ============================================================

orders = [
    {
        "order_id": "ORD001",
        "product": "Component-A",
        "quantity": 500,
        "available_hours": 4,
        "priority": "HIGH"
    },

    {
        "order_id": "ORD002",
        "product": "Component-B",
        "quantity": 700,
        "available_hours": 5,
        "priority": "MEDIUM"
    },

    {
        "order_id": "ORD003",
        "product": "Component-C",
        "quantity": 400,
        "available_hours": 6,
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
# NORMALIZE ENERGY
# ============================================================

minimum_energy = min(
    energy_per_unit.values()
)

maximum_energy = max(
    energy_per_unit.values()
)


def energy_score(machine_id):

    energy = energy_per_unit[machine_id]

    if maximum_energy == minimum_energy:

        return 100

    score = (
        (maximum_energy - energy)
        /
        (maximum_energy - minimum_energy)
    ) * 100

    return score


# ============================================================
# MULTI-OBJECTIVE SCORING
# ============================================================

def calculate_score(
    machine_id,
    quantity,
    available_hours
):

    health = machine_health[machine_id]

    capacity = machines[machine_id][
        "capacity_per_hour"
    ]

    energy = energy_per_unit[machine_id]


    # --------------------------------------------------------
    # Production time
    # --------------------------------------------------------

    production_time = (
        quantity / capacity
    )


    # --------------------------------------------------------
    # Health score
    # --------------------------------------------------------

    if health == "NORMAL":

        health_score = 100

    elif health == "MONITOR":

        health_score = 60

    else:

        health_score = 0


    # --------------------------------------------------------
    # Capacity / deadline score
    # --------------------------------------------------------

    if production_time <= available_hours:

        deadline_score = 100

    else:

        deadline_score = 0


    # --------------------------------------------------------
    # Energy score
    # --------------------------------------------------------

    efficiency_score = energy_score(
        machine_id
    )


    # --------------------------------------------------------
    # Production speed score
    # --------------------------------------------------------

    maximum_capacity = max(
        machine["capacity_per_hour"]
        for machine in machines.values()
    )


    capacity_score = (
        capacity
        /
        maximum_capacity
    ) * 100


    # --------------------------------------------------------
    # FINAL SCORE
    # --------------------------------------------------------

    final_score = (
        health_score * 0.40
        +
        efficiency_score * 0.30
        +
        deadline_score * 0.20
        +
        capacity_score * 0.10
    )


    return {
        "machine": machine_id,
        "health": health,
        "energy": energy,
        "production_time": production_time,
        "health_score": health_score,
        "efficiency_score": efficiency_score,
        "deadline_score": deadline_score,
        "capacity_score": capacity_score,
        "final_score": final_score
    }


# ============================================================
# DISPLAY HEADER
# ============================================================

print("\n" + "=" * 95)
print("AI FACTORY ENERGY COPILOT")
print("MULTI-OBJECTIVE PRODUCTION OPTIMIZATION")
print("=" * 95)


# ============================================================
# PROCESS ORDERS
# ============================================================

for order in orders:

    print("\n" + "=" * 95)

    print(
        f"ORDER: {order['order_id']}"
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
        f"Available production time: "
        f"{order['available_hours']} hours"
    )

    print("-" * 95)


    candidates = []


    for machine_id in machines:

        health = machine_health.get(
            machine_id,
            "UNKNOWN"
        )

        # HIGH-RISK machines are never considered.

        if health == "HIGH_RISK":

            print(
                f"{machine_id} → "
                f"AVOID | HIGH_RISK"
            )

            continue


        result = calculate_score(
            machine_id,
            order["quantity"],
            order["available_hours"]
        )


        candidates.append(result)


        print(
            f"{machine_id} → "
            f"Health={result['health']} | "
            f"Energy={result['energy']:.6f} kWh/unit | "
            f"Time={result['production_time']:.2f} h | "
            f"Score={result['final_score']:.2f}"
        )


    # --------------------------------------------------------
    # SELECT BEST MACHINE
    # --------------------------------------------------------

    valid_candidates = [
        candidate
        for candidate in candidates
        if candidate["deadline_score"] > 0
    ]


    if not valid_candidates:

        print("\n⚠️ No machine can satisfy the deadline.")

        continue


    recommendation = max(
        valid_candidates,
        key=lambda candidate:
        candidate["final_score"]
    )


    # ========================================================
    # RECOMMENDATION
    # ========================================================

    print("\n" + "-" * 95)

    print("AI RECOMMENDATION")

    print(
        f"Machine: "
        f"{recommendation['machine']}"
    )

    print(
        f"Health: "
        f"{recommendation['health']}"
    )

    print(
        f"Energy intensity: "
        f"{recommendation['energy']:.6f} kWh/unit"
    )

    print(
        f"Production time: "
        f"{recommendation['production_time']:.2f} hours"
    )

    print(
        f"Decision score: "
        f"{recommendation['final_score']:.2f}/100"
    )


    print("\nDecision factors:")

    print(
        f"  Health score: "
        f"{recommendation['health_score']:.1f}"
    )

    print(
        f"  Energy score: "
        f"{recommendation['efficiency_score']:.1f}"
    )

    print(
        f"  Deadline score: "
        f"{recommendation['deadline_score']:.1f}"
    )

    print(
        f"  Capacity score: "
        f"{recommendation['capacity_score']:.1f}"
    )


    print("\nReason:")

    print(
        "  ✓ Machine is not HIGH_RISK"
    )

    print(
        "  ✓ Production can meet the deadline"
    )

    print(
        "  ✓ Energy efficiency considered"
    )

    print(
        "  ✓ Production capacity considered"
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 95)
print("MULTI-OBJECTIVE OPTIMIZATION COMPLETE")
print("=" * 95)