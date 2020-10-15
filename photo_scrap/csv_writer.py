from __future__ import annotations  # for type hints of typed lists
from pathlib import Path
import os
import nested_csv


def to_csv(items: list[dict], csv_filepath: str, default_columns: list[str]) -> bool:
    csv_columns = nested_csv.generate_fieldnames(
        items[0]) if items else default_columns
    key = 'id'
    csv_columns.remove(key)
    csv_columns.insert(0, key)
    Path(os.path.dirname(csv_filepath)).mkdir(
        parents=True, exist_ok=True)
    try:
        with open(csv_filepath, 'w') as csvfile:
            writer = nested_csv.NestedDictWriter(
                csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for item in items:
                writer.writerow(item)
    except IOError:
        print("File write error")
        return False
    return True
