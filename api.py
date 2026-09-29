from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import csv
from collections import defaultdict
from pathlib import Path

app = FastAPI(
    title="AI Factory Energy Copilot API",
    description="Backend API for the AI Factory Energy Copilot prototype",
    version="1.0.0"
)

# Allow React/Vite frontend to communicate with Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
CSV_FILE = BASE_DIR / "factory_data.csv"


def load_factory_data():
    """Load simulated factory telemetry from CSV."""

    if not CSV_FILE.exists():
        raise FileNotFoundError(
            f"Factory data file not found: {CSV_FILE}"
        )

    with open(CSV_FILE, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)


def calculate_machine_data(rows):
    """Calculate machine-level intelligence from telemetry."""

    machines = defaultdict(list)

    for row in rows:
        machines[row["machine_id"]].append(row)

    results = []

    for machine_id, machine_rows in machines.items():

        abnormal_events = sum(
            1
            for row in machine_rows
            if row["state"] == "ABNORMAL"
        )

        high_load_events = sum(
            1
            for row in machine_rows
            if row["state"] == "HIGH_LOAD"
        )

        total_energy = 0.0
        total_production = 0

        for row in machine_rows:
            power_kw = float(row["power_kw"])
            production = int(row["production_units"])

            # Each telemetry record represents approximately 2 seconds.
            energy_kwh = power_kw * (2 / 3600)

            total_energy += energy_kwh
            total_production += production

        if total_production > 0:
            energy_per_unit = total_energy / total_production
        else:
            energy_per_unit = 0

        # Health classification
        if abnormal_events > 0:
            health = "HIGH_RISK"
        elif high_load_events > 0:
            health = "MONITOR"
        else:
            health = "NORMAL"

        results.append(
            {
                "machine_id": machine_id,
                "health": health,
                "abnormal_events": abnormal_events,
                "high_load_events": high_load_events,
                "energy_per_unit": round(energy_per_unit, 6),
                "total_energy": round(total_energy, 4),
                "total_production": total_production,
            }
        )

    return sorted(
        results,
        key=lambda machine: machine["machine_id"]
    )


@app.get("/")
def root():
    return {
        "system": "AI Factory Energy Copilot",
        "status": "online",
        "mode": "simulation",
        "message": "Factory intelligence API is running"
    }


@app.get("/api/health")
def api_health():
    return {
        "status": "healthy",
        "service": "AI Factory Energy Copilot API"
    }


@app.get("/api/factory")
def factory_overview():

    rows = load_factory_data()
    machines = calculate_machine_data(rows)

    high_risk = [
        machine
        for machine in machines
        if machine["health"] == "HIGH_RISK"
    ]

    return {
        "machines_monitored": len(machines),
        "machines": machines,
        "high_risk_count": len(high_risk),
        "high_risk_machines": [
            machine["machine_id"]
            for machine in high_risk
        ],
    }


@app.get("/api/machines")
def machine_health():

    rows = load_factory_data()

    return {
        "machines": calculate_machine_data(rows)
    }


@app.get("/api/anomalies")
def anomalies():

    rows = load_factory_data()

    abnormal_rows = [
        {
            "timestamp": row["timestamp"],
            "machine_id": row["machine_id"],
            "state": row["state"],
            "power_kw": float(row["power_kw"]),
            "temperature_c": float(row["temperature_c"]),
            "vibration_mm_s": float(row["vibration_mm_s"]),
            "rpm": int(row["rpm"]),
            "production_units": int(row["production_units"]),
        }
        for row in rows
        if row["state"] == "ABNORMAL"
    ]

    return {
        "total_abnormal_events": len(abnormal_rows),
        "events": abnormal_rows,
    }


@app.get("/api/energy")
def energy_analysis():

    rows = load_factory_data()
    machines = calculate_machine_data(rows)

    total_energy = sum(
        machine["total_energy"]
        for machine in machines
    )

    total_production = sum(
        machine["total_production"]
        for machine in machines
    )

    energy_per_unit = (
        total_energy / total_production
        if total_production > 0
        else 0
    )

    return {
        "total_energy_kwh": round(total_energy, 4),
        "total_production_units": total_production,
        "overall_energy_per_unit": round(
            energy_per_unit,
            6
        ),
        "machines": [
            {
                "machine_id": machine["machine_id"],
                "energy_per_unit": machine["energy_per_unit"],
                "total_energy": machine["total_energy"],
                "total_production": machine["total_production"],
            }
            for machine in machines
        ],
    }


@app.get("/api/orders")
def production_orders():

    # Current prototype orders
    orders = [
        {
            "order_id": "ORD001",
            "product": "Component-A",
            "quantity": 500,
            "priority": "HIGH",
            "machine": "M01",
            "time_hours": 1.67,
            "energy_kwh": 0.0521,
            "score": 71.96,
        },
        {
            "order_id": "ORD002",
            "product": "Component-B",
            "quantity": 700,
            "priority": "MEDIUM",
            "machine": "M01",
            "time_hours": 2.33,
            "energy_kwh": 0.0729,
            "score": 60.30,
        },
        {
            "order_id": "ORD003",
            "product": "Component-C",
            "quantity": 400,
            "priority": "LOW",
            "machine": "M03",
            "time_hours": 1.14,
            "energy_kwh": 0.0745,
            "score": 64.29,
        },
    ]

    return {
        "total_orders": len(orders),
        "total_production": sum(
            order["quantity"]
            for order in orders
        ),
        "orders": orders,
    }


@app.get("/api/impact")
def impact_analysis():

    production_energy = 0.1995

    # Prototype assumptions used by the current analysis.
    electricity_rate = 8.0
    co2_factor = 0.70

    electricity_cost = production_energy * electricity_rate
    co2_emissions = production_energy * co2_factor

    return {
        "production_energy_kwh": production_energy,
        "electricity_cost_inr": round(electricity_cost, 2),
        "co2_emissions_kg": round(co2_emissions, 4),
    }


@app.get("/api/dashboard")
def dashboard():

    rows = load_factory_data()
    machines = calculate_machine_data(rows)

    orders = [
        {
            "order_id": "ORD001",
            "product": "Component-A",
            "quantity": 500,
            "priority": "HIGH",
            "machine": "M01",
            "time_hours": 1.67,
            "energy_kwh": 0.0521,
            "score": 71.96,
        },
        {
            "order_id": "ORD002",
            "product": "Component-B",
            "quantity": 700,
            "priority": "MEDIUM",
            "machine": "M01",
            "time_hours": 2.33,
            "energy_kwh": 0.0729,
            "score": 60.30,
        },
        {
            "order_id": "ORD003",
            "product": "Component-C",
            "quantity": 400,
            "priority": "LOW",
            "machine": "M03",
            "time_hours": 1.14,
            "energy_kwh": 0.0745,
            "score": 64.29,
        },
    ]

    abnormal_events = sum(
        machine["abnormal_events"]
        for machine in machines
    )

    high_risk_machines = [
        machine["machine_id"]
        for machine in machines
        if machine["health"] == "HIGH_RISK"
    ]

    total_production = sum(
        order["quantity"]
        for order in orders
    )

    total_energy = sum(
        order["energy_kwh"]
        for order in orders
    )

    electricity_cost = total_energy * 8
    co2 = total_energy * 0.70

    return {
        "mode": "SIMULATION",
        "machines_monitored": len(machines),
        "planned_production": total_production,
        "production_energy_kwh": round(total_energy, 4),
        "high_risk_machines": high_risk_machines,
        "high_risk_count": len(high_risk_machines),
        "abnormal_events": abnormal_events,
        "electricity_cost": round(electricity_cost, 2),
        "co2_emissions": round(co2, 4),
        "machines": machines,
        "orders": orders,
    }