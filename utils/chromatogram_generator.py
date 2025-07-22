
import random

def generate_peaks(
    compounds=None,
    faults=None,
    shift_rt=False,
    baseline_noise=False,
    coelution=False
):
    faults = faults or []
    compounds = compounds or [
        {"name": "Methane", "rt": 1.2},
        {"name": "Ethane", "rt": 1.6},
        {"name": "Propane", "rt": 2.1},
        {"name": "i-Butane", "rt": 2.8},
        {"name": "n-Butane", "rt": 3.1}
    ]

    peaks = []
    for compound in compounds:
        rt = compound["rt"]
        if shift_rt:
            rt += random.uniform(-0.05, 0.05)

        area = random.randint(1000, 3000)
        height = area / random.uniform(4, 10)
        width = area / height / 1.8

        peak = {
            "name": compound["name"],
            "rt": round(rt, 3),
            "area": int(area),
            "height": int(height),
            "width": round(width, 3)
        }

        if "tailing" in faults:
            peak["tailing_factor"] = round(random.uniform(1.5, 2.5), 2)
        if "fronting" in faults:
            peak["fronting_factor"] = round(random.uniform(0.5, 0.9), 2)
        if coelution and compound["name"] == "Ethane":
            peaks.append({
                "name": "Unknown",
                "rt": round(rt + 0.02, 3),
                "area": int(area * 0.7),
                "height": int(height * 0.6),
                "width": round(width * 1.2, 3)
            })

        peaks.append(peak)

    if baseline_noise:
        for i in range(3):
            peaks.append({
                "name": f"Noise_{i+1}",
                "rt": round(random.uniform(0.5, 4.5), 3),
                "area": random.randint(20, 100),
                "height": random.randint(5, 20),
                "width": round(random.uniform(0.05, 0.1), 3)
            })

    return sorted(peaks, key=lambda p: p["rt"])
