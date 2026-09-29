import random
from datetime import datetime


# --------------------------------------------------
# MACHINE INFORMATION
# --------------------------------------------------

machines = {
    "M01": {
        "capacity_per_hour": 300,
        "energy_per_unit": 0.014,
        "efficiency": 0.92
    },

    "M02": {
        "capacity_per_hour": 250,
        "energy_per_unit": 0.018,
        "efficiency": 0.86
    },

    "M03": {
        "capacity_per_hour": 350,
        "energy_per_unit": 0.012,
        "efficiency": 0.95
    }
}


# --------------------------------------------------
# PRODUCTION ORDERS
# --------------------------------------------------

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


# --------------------------------------------------
# DISPLAY FACTORY MACHINES
# --------------------------------------------------

print("\n" + "=" * 80)
print("AI FACTORY ENERGY COPILOT")
print("FACTORY MACHINE CAPABILITIES")
print("=" * 80)


for machine_id, machine in machines.items():

    print(f"\nMachine: {machine_id}")

    print(
        f"Capacity       : "
        f"{machine['capacity_per_hour']} units/hour"
    )

    print(
        f"Energy/Unit    : "
        f"{machine['energy_per_unit']} kWh/unit"
    )

    print(
        f"Efficiency     : "
        f"{machine['efficiency'] * 100:.1f}%"
    )


# --------------------------------------------------
# DISPLAY PRODUCTION ORDERS
# --------------------------------------------------

print("\n" + "=" * 80)
print("CURRENT PRODUCTION ORDERS")
print("=" * 80)


for order in orders:

    print(f"\nOrder ID       : {order['order_id']}")
    print(f"Product        : {order['product']}")
    print(f"Quantity       : {order['quantity']} units")
    print(f"Deadline       : {order['deadline']}")
    print(f"Priority       : {order['priority']}")


# --------------------------------------------------
# BASIC PRODUCTION PLANNING
# --------------------------------------------------

print("\n" + "=" * 80)
print("BASIC PRODUCTION PLANNING")
print("=" * 80)


for order in orders:

    print(
        f"\n{order['order_id']} "
        f"({order['quantity']} units)"
    )

    for machine_id, machine in machines.items():

        production_hours = (
            order["quantity"]
            / machine["capacity_per_hour"]
        )

        estimated_energy = (
            order["quantity"]
            * machine["energy_per_unit"]
        )

        print(
            f"  {machine_id} → "
            f"{production_hours:.2f} hours | "
            f"{estimated_energy:.2f} kWh"
        )