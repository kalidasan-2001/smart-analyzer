import os
import csv
import time
import random
from datetime import datetime, timezone
from pathlib import Path

def get_env_var(name, default, cast_func):
    val = os.environ.get(name, default)
    try:
        return cast_func(val)
    except Exception:
        return cast_func(default)

def generate_row():
    # Base values and noise
    base_temp = 24.5
    temp_noise = random.gauss(0, 0.6)
    base_vib = 0.12
    vib_noise = random.gauss(0, 0.04)

    # Anomaly spikes
    temp_spike = 0
    vib_spike = 0
    if random.random() < SPIKE_PROB:
        if random.choice([True, False]):
            temp_spike = random.uniform(2.5, 3.5)
        else:
            vib_spike = random.uniform(0.22, 0.28)

    temp = round(base_temp + temp_noise + temp_spike, 2)
    vib = round(base_vib + vib_noise + vib_spike, 3)
    timestamp = datetime.now(timezone.utc).isoformat(timespec='seconds')
    return [timestamp, temp, vib]

def rotate_file(path, max_rows=1000):
    # Keep only last max_rows rows (plus header)
    with path.open("r", newline='') as f:
        reader = list(csv.reader(f))
    header, rows = reader[0], reader[1:]
    if len(rows) > max_rows:
        rows = rows[-max_rows:]
        with path.open("w", newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(rows)

def main():
    # Print startup message
    print(f"Sensor simulator started. Writing to: {DATA_PATH.resolve()}")
    header = ["timestamp", "temperature", "vibration"]

    while True:
        row = generate_row()
        file_exists = DATA_PATH.exists()
        # Write row
        with DATA_PATH.open("a", newline='') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(header)
            writer.writerow(row)
        print(f"Written: {dict(zip(header, row))}")
        # Rotate file if needed
        try:
            rotate_file(DATA_PATH, max_rows=1000)
        except Exception as e:
            print(f"File rotation error: {e}")
        time.sleep(INTERVAL_SEC)

if __name__ == "__main__":
    # Read env vars
    DATA_PATH = Path(os.environ.get("DATA_PATH", "./data.csv")).resolve()
    INTERVAL_SEC = get_env_var("INTERVAL_SEC", 2, float)
    SPIKE_PROB = get_env_var("SPIKE_PROB", 0.03, float)
    main()