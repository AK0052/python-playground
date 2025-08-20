import json
import csv
from pathlib import Path

try:

    with open("config.json", "r") as f:
        config = json.load(f)

    print("loading config ...", config)

    input_file = Path(config["input_file"])
    if not input_file.exists:
        raise FileNotFoundError(f"Input file not found: {input_file}")
    rows = []

    with input_file.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)

    print(f"Loaded {len(rows)} rows from {input_file}")
    print("First row:", rows[0] if rows else None)

    filtered_rows = []

    for row in rows:
        try:
            age = int(row["age"])
        except ValueError:
            print(f"Skipping row with invalid age: {row}")
            continue

        if age >= config["min_age"]:
            filtered_row = {col: row[col] for col in config["columns"]}
            filtered_rows.append(filtered_row)

    print(f"Filtered down to {len(filtered_rows)} rows")
    print("Example filtered row:", filtered_rows[0] if filtered_rows else None)

    output_file = Path(config["output_file"])

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=config["columns"])
        writer.writeheader()
        writer.writerows(filtered_rows)


    print(f"Saved {len(filtered_rows)} rows to {output_file}")

except Exception as err:
    print(f"Error: {err}")
    sys.exit(1)
