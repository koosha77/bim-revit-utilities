"""
DIN 276 cost-group mapping helpers.

Maps Revit / DBD-BIM element categories to DIN 276-1 cost groups
(Kostengruppen). Focus on KG 300 (Bauwerk – Baukonstruktionen) and
KG 400 (Bauwerk – Technische Anlagen), which dominate building costs.

Reference: DIN 276:2018-12.

Author: Koosha Karamian, THD Deggendorf
"""

from __future__ import annotations

from dataclasses import dataclass

# Selection of common cost groups relevant to civil / structural work
DIN276_GROUPS: dict[str, str] = {
    "310": "Baugrube / Erdbau",
    "320": "Gründung, Unterbau",
    "330": "Außenwände, vertikale Baukonstruktionen",
    "340": "Innenwände, vertikale Baukonstruktionen",
    "350": "Decken, horizontale Baukonstruktionen",
    "360": "Dächer",
    "370": "Infrastrukturanlagen",
    "390": "Sonstige Maßnahmen für Baukonstruktionen",
    "410": "Abwasser-, Wasser-, Gasanlagen",
    "420": "Wärmeversorgungsanlagen",
    "430": "Raumlufttechnische Anlagen",
    "440": "Elektrische Anlagen",
}

# Default mapping from Revit categories to DIN 276 KG
REVIT_TO_DIN276 = {
    "Walls":         "330",   # treat as exterior unless interior detected
    "Walls_Interior": "340",
    "Floors":        "350",
    "Roofs":         "360",
    "Foundation":    "320",
    "StructuralColumns": "330",
    "Ducts":         "430",
    "PipingSystems": "410",
    "ElectricalEquipment": "440",
}


@dataclass
class CostLine:
    revit_category: str
    kg_code: str
    kg_name: str
    quantity: float
    unit: str


def map_element(revit_category: str, quantity: float, unit: str) -> CostLine:
    kg = REVIT_TO_DIN276.get(revit_category, "390")
    return CostLine(revit_category, kg, DIN276_GROUPS[kg], quantity, unit)


if __name__ == "__main__":
    demo = [
        ("Walls", 124.5, "m²"),
        ("Floors", 240.0, "m²"),
        ("Roofs", 130.0, "m²"),
        ("Foundation", 32.0, "m³"),
        ("PipingSystems", 85.0, "m"),
    ]
    for cat, qty, unit in demo:
        line = map_element(cat, qty, unit)
        print(f"{line.kg_code} {line.kg_name:<45} {line.quantity:>7.1f} {line.unit}")
