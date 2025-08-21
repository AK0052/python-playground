from __future__ import annotations
import json
import csv
import sys
from pathlib import Path
from typing import List, Dict, Any

TYPE_CASTERS = {
    "int": int,
    "float": float,
    "str": str
}

def cast_row(row: Dict[str, str], schema: Dict[str, str]) -> Dict[str, Any]:
    casted = {}
    for key, value in row.items():
        if key in schema:
            caster = TYPE_CASTERS.get(schema[key])
            try:
                casted[key] = caster(value)
            except (ValueError, TypeError):
                casted[key] = None
        else:
            casted[key] = value
    return casted

def load_config(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)
    
def read_csv(path: Path, schema: Dict[str, str]) -> List[Dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Input file not found: {path}")
    rows: List[Dict[str, str]] = []
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            casted_row = cast_row(row, schema)
            rows.append(row)
    return rows

def filter_rows(
        rows: List[Dict[str, str]],
        columns: List[str],
        min_age: int,
) -> List[Dict[str, str]]:
    filtered: List[Dict[str, str]] =[]
    for row in rows:
        try:
            age = int(row.get("age", "").strip())
        except (ValueError, AttributeError):
            # skip bad rows but continue processing
            print(f"Skipping row with invalid age: {row}")
            continue

        if age >= min_age:
            filtered.append({col: row[col] for col in columns if col in row})
    return filtered

def write_csv(path: Path, rows: List[Dict[str, str]], columns: List[str, str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)

def main() -> int:
    try:
        config = load_config(Path("config.json"))
        input_file = Path(config["input_file"])
        output_file = Path(config["output_file"])
        columns = list(config["columns"])
        min_age = int(config["min_age"])

        schema = config.get("schema", {})
        rows = read_csv(input_file, schema)
        filtered = filter_rows(rows, columns, min_age)
        write_csv(output_file, filtered, columns)

        print(f"✅ Done: saved {len(filtered)} rows to {output_file}")
        return 0
    except Exception as err:
        print(f"Error: {err}")
        return 1
    
if __name__ == "__main__":
    sys.exit(main())
