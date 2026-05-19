"""
Parse Revit schedule CSV exports into a clean pandas DataFrame.

Revit schedule exports often contain:
  - a title row
  - merged header rows
  - thousands separators with commas
  - units appended to values (e.g. '12.50 m²')

This module normalizes those quirks.

Author: Koosha Karamian, THD Deggendorf
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

_UNIT_RE = re.compile(r"\s*(m²|m³|m|mm|kg|Stück|pcs)\s*$", re.IGNORECASE)


def _strip_unit(value: str) -> float | str:
    if not isinstance(value, str):
        return value
    cleaned = _UNIT_RE.sub("", value).strip().replace(",", ".")
    try:
        return float(cleaned)
    except ValueError:
        return value


def load_schedule(csv_path: str | Path, skip_title_rows: int = 1) -> pd.DataFrame:
    """Read a Revit schedule CSV and return a tidy DataFrame."""
    df = pd.read_csv(csv_path, skiprows=skip_title_rows, sep=None, engine="python")
    df.columns = [c.strip() for c in df.columns]
    df = df.dropna(how="all")
    return df.map(_strip_unit)


def total_quantity(df: pd.DataFrame, column: str) -> float:
    return float(pd.to_numeric(df[column], errors="coerce").sum())


if __name__ == "__main__":
    # Tiny demo with an inline CSV
    import io

    sample = io.StringIO(
        "Wall Schedule\n"
        "Type,Length,Area\n"
        "Exterior - 30 cm,\"12,50 m\",\"31,25 m²\"\n"
        "Interior - 11.5 cm,\"8,00 m\",\"20,00 m²\"\n"
    )
    df = load_schedule(sample, skip_title_rows=1)
    print(df)
    print("Total area:", total_quantity(df, "Area"), "m²")
