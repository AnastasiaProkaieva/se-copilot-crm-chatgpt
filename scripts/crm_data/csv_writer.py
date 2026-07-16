"""Writes a list of flat dicts to a CSV file with a header row."""

import csv


def write_csv(rows: list[dict], path: str) -> None:
    if not rows:
        raise ValueError(f"Cannot write CSV with no rows: {path}")

    fieldnames = list(rows[0].keys())
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
