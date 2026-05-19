# bim-revit-utilities

Small Python helpers and notes around **BIM workflows** with Autodesk Revit and **DBD-BIM** integration. Created during my Master's program in Civil & Environmental Engineering at **Technische Hochschule Deggendorf**.

## Scope

Lightweight tools to support BIM-based coursework and (later) thesis work:

- Parse Revit schedule CSV exports into clean pandas DataFrames
- Quantity take-off helpers for walls, floors, and structural elements
- Mapping between Revit element parameters and DBD-BIM cost positions
- Helpers around HOAI service phases and DIN 276 cost groups (KG 300/400)

## Folder layout

```
bim-revit-utilities/
├── schedules/        # Parsers for Revit schedule exports
├── quantities/       # Quantity take-off utilities
├── costs/            # DIN 276 / HOAI helpers
└── notes/            # Markdown notes on BIM workflows (DE/EN)
```

## Why

Most BIM courses focus on the GUI side of Revit. This repo is my place to script the boring bits — cleaning schedules, normalizing units (m², m³, kg), and connecting model data to German cost frameworks. Goal: less Excel copy-paste, more reproducible workflows.

## Tech

- Python 3.11+
- pandas, openpyxl
- (Optional) pyRevit / Dynamo for in-Revit scripts

## License

MIT — see [LICENSE](LICENSE).
