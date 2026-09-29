import csv
from collections import defaultdict


CSV_FILE = "factory_data.csv"


# --------------------------------------------------
# STORE MACHINE DATA
# --------------------------------------------------

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
            "rpm": int(row["rpm"]),
            "production": int(row["production_units"])
        })


# --------------------------------------------------
# LEARN NORMAL MACHINE BEHAVIOR
# --------------------------------------------------

normal_profiles = {}


for machine_id, readings in machine_data.items():

    normal_readings = [
        reading
        for reading in readings
        if reading["state"] == "NORMAL"
    ]

    if not normal_readings:
        continue

    normal_profiles[machine_id] = {

        "power": sum(
            r["power"] for r in normal_readings
        ) / len(normal_readings),

        "temperature": sum(
            r["temperature"] for r in normal_readings
        ) / len(normal_readings),

        "vibration": sum(
            r["vibration"] for r in normal_readings
        ) / len(normal_readings),

        "rpm": sum(
            r["rpm"] for r in normal_readings
        ) / len(normal_readings),

        "production": sum(
            r["production"] for r in normal_readings
        ) / len(normal_readings)
    }


# --------------------------------------------------
# DETECTION THRESHOLDS
# --------------------------------------------------

POWER_LIMIT = 1.30
TEMPERATURE_LIMIT = 1.30
VIBRATION_LIMIT = 1.80
RPM_LIMIT = 0.85
PRODUCTION_LIMIT = 0.60


# --------------------------------------------------
# DISPLAY RESULTS
# --------------------------------------------------

print("\n" + "=" * 80)
print("AI FACTORY ENERGY COPILOT")
print("MACHINE ANOMALY DETECTION")
print("=" * 80)


anomalies_found = 0


for machine_id, readings in machine_data.items():

    if machine_id not in normal_profiles:
        continue

    profile = normal_profiles[machine_id]

    print(f"\nMachine: {machine_id}")
    print("-" * 80)

    for reading in readings:

        # ------------------------------------------
        # Only investigate abnormal operating state
        # ------------------------------------------

        if reading["state"] != "ABNORMAL":
            continue

        power_ratio = (
            reading["power"] / profile["power"]
        )

        temperature_ratio = (
            reading["temperature"] /
            profile["temperature"]
        )

        vibration_ratio = (
            reading["vibration"] /
            profile["vibration"]
        )

        rpm_ratio = (
            reading["rpm"] /
            profile["rpm"]
        )

        production_ratio = (
            reading["production"] /
            profile["production"]
        )


        # ------------------------------------------
        # Calculate anomaly score
        # ------------------------------------------

        score = 0

        reasons = []


        if power_ratio > POWER_LIMIT:

            score += 1

            reasons.append(
                "Power consumption significantly increased"
            )


        if temperature_ratio > TEMPERATURE_LIMIT:

            score += 1

            reasons.append(
                "Temperature significantly increased"
            )


        if vibration_ratio > VIBRATION_LIMIT:

            score += 1

            reasons.append(
                "Vibration significantly increased"
            )


        if rpm_ratio < RPM_LIMIT:

            score += 1

            reasons.append(
                "RPM significantly decreased"
            )


        if production_ratio < PRODUCTION_LIMIT:

            score += 1

            reasons.append(
                "Production output significantly decreased"
            )


        # ------------------------------------------
        # Determine risk level
        # ------------------------------------------

        if score >= 4:

            risk = "HIGH"

        elif score >= 2:

            risk = "MEDIUM"

        else:

            risk = "LOW"


        # ------------------------------------------
        # Display anomaly
        # ------------------------------------------

        print("\n⚠️ ANOMALY DETECTED")

        print(
            f"Timestamp       : {reading['timestamp']}"
        )

        print(
            f"State           : {reading['state']}"
        )

        print(
            f"Power           : {reading['power']:.2f} kW"
        )

        print(
            f"Temperature     : "
            f"{reading['temperature']:.2f} °C"
        )

        print(
            f"Vibration       : "
            f"{reading['vibration']:.2f} mm/s"
        )

        print(
            f"RPM             : {reading['rpm']}"
        )

        print(
            f"Production      : "
            f"{reading['production']} units"
        )

        print(
            f"Anomaly Score   : {score}/5"
        )

        print(
            f"Risk Level      : {risk}"
        )

        print("\nDetected Indicators:")

        for reason in reasons:

            print(f"  • {reason}")


        print(
            "\nRecommended Action:"
        )

        if risk == "HIGH":

            print(
                "  Inspect machine M02 before "
                "continuing normal production."
            )

        elif risk == "MEDIUM":

            print(
                "  Monitor machine closely and "
                "schedule inspection."
            )

        else:

            print(
                "  Continue monitoring machine."
            )


        anomalies_found += 1


# --------------------------------------------------
# FINAL SUMMARY
# --------------------------------------------------

print("\n" + "=" * 80)

print(
    f"Total abnormal events detected: "
    f"{anomalies_found}"
)

print("=" * 80)