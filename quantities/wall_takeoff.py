"""
Wall quantity take-off.

Given a DataFrame of walls (type, length, height, thickness) plus a list
of openings (windows, doors) per wall, compute net area and net volume.

Useful as a sanity check on Revit / DBD-BIM schedule exports.

Author: Koosha Karamian, THD Deggendorf
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass
class WallQuantities:
    wall_id: str
    gross_area_m2: float
    openings_area_m2: float
    net_area_m2: float
    net_volume_m3: float


def compute_wall(
    wall_id: str,
    length_m: float,
    height_m: float,
    thickness_m: float,
    openings_m2: list[float] | None = None,
) -> WallQuantities:
    openings_m2 = openings_m2 or []
    gross = length_m * height_m
    open_area = sum(openings_m2)
    net = max(gross - open_area, 0.0)
    volume = net * thickness_m
    return WallQuantities(wall_id, gross, open_area, net, volume)


def compute_from_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Expect columns: id, length_m, height_m, thickness_m, openings_m2 (list)."""
    rows = [
        compute_wall(
            row["id"],
            row["length_m"],
            row["height_m"],
            row["thickness_m"],
            row.get("openings_m2") or [],
        )
        for _, row in df.iterrows()
    ]
    return pd.DataFrame([r.__dict__ for r in rows])


if __name__ == "__main__":
    walls = pd.DataFrame(
        [
            dict(id="W-01", length_m=6.0, height_m=2.8, thickness_m=0.30,
                 openings_m2=[1.2 * 1.4]),  # one window
            dict(id="W-02", length_m=4.5, height_m=2.8, thickness_m=0.115,
                 openings_m2=[0.9 * 2.1]),  # one door
        ]
    )
    print(compute_from_dataframe(walls).to_string(index=False))
