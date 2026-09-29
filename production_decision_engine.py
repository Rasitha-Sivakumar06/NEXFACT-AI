import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"


# --------------------------------------------------
# MACHINE CONFIGURATION
# --------------------------------------------------

machines = {
    "M01": {
        "capacity_per_hour": 300,
        "energy_per_unit": 0.014
    },

    "M02": {
        "capacity_per_hour": 250,
        "energy_per_unit": 0.018
    },

    "M03": {
        "capacity_per_hour": 350,
        "energy_per_unit": 0.012
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
# READ FACTORY DATA
# --------------------------------------------------

latest_data = {}

abnormal_machines = set()


with open(CSV_FILE, "r") as file:

    reader = csv.DictReader(file)

    for row in reader:

        machine_id = row["machine_id"]

        latest_data[machine_id] = {
            "state": row["state"],
            "power": float(row["power_kw"]),
            "temperature": float(row["temperature_c"]),
            "vibration": float(row["vibration_mm_s"]),
            "production": int(row["production_units"])
        }

        if row["state"] == "ABNORMAL":

            abnormal_machines.add(machine_id)


# --------------------------------------------------
# DISPLAY CURRENT MACHINE STATUS
# --------------------------------------------------

print("\n" + "=" * 80)
print("AI FACTORY ENERGY COPILOT")
print("MACHINE-AWARE PRODUCTION DECISION ENGINE")
print("=" * 80)


for machine_id in machines:

    data = latest_data.get(machine_id)

    print(f"\nMachine: {machine_id}")

    if machine_id in abnormal_machines:

        print("Status: ⚠️ HIGH RISK")

    elif data and data["state"] == "IDLE":

        print("Status: IDLE")

    else:

        print("Status: AVAILABLE")


# --------------------------------------------------
# PRODUCTION DECISION
# --------------------------------------------------

print("\n" + "=" * 80)
print("PRODUCTION ASSIGNMENT ANALYSIS")
print("=" * 80)


for order in orders:

    print(
        f"\nOrder {order['order_id']} | "
        f"{order['product']} | "
        f"{order['quantity']} units | "
        f"Priority: {order['priority']}"
    )

    candidates = []

    for machine_id, machine in machines.items():

        # ------------------------------------------
        # Skip machines with abnormal behavior
        # ------------------------------------------

        if machine_id in abnormal_machines:

            print(
                f"  {machine_id} → "
                f"NOT RECOMMENDED "
                f"(machine health risk)"
            )

            continue


        # ------------------------------------------
        # Calculate production time
        # ------------------------------------------

        production_hours = (
            order["quantity"]
            / machine["capacity_per_hour"]
        )


        # ------------------------------------------
        # Calculate energy
        # ------------------------------------------

        estimated_energy = (
            order["quantity"]
            * machine["energy_per_unit"]
        )


        # ------------------------------------------
        # Create candidate
        # ------------------------------------------

        candidates.append({
            "machine": machine_id,
            "hours": production_hours,
            "energy": estimated_energy
        })


        print(
            f"  {machine_id} → "
            f"{production_hours:.2f} hours | "
            f"{estimated_energy:.2f} kWh"
        )


    # --------------------------------------------------
    # Select energy-efficient healthy machine
    # --------------------------------------------------

    if candidates:

        best_machine = min(
            candidates,
            key=lambda x: x["energy"]
        )

        print(
            f"\n  → Recommended machine: "
            f"{best_machine['machine']}"
        )

        print(
            f"    Estimated energy: "
            f"{best_machine['energy']:.2f} kWh"
        )

        print(
            f"    Production time: "
            f"{best_machine['hours']:.2f} hours"
        )


print("\n" + "=" * 80)
print("DECISION ENGINE COMPLETE")
print("=" * 80)