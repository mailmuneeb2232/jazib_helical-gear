# Helical Gear Calculator

A professional **Python / Flask** web application for helical gear design and analysis using the **Pitch Diameter (PD) based method** with **inch units**.

---

## Features

| Feature | Detail |
|---|---|
| Calculation method | PD-based, inch units throughout |
| Inputs | 10 parameters (geometry, operating conditions, gear pair, load factor) |
| Outputs | 10 selectable parameters with user-controlled display |
| UI | Modern dark engineering dashboard — glassmorphism, animated cards, Chart.js visualisation |
| Export | PDF report (ReportLab) + Excel report (openpyxl) |
| Save / Load | JSON project files (download / upload) |
| Validation | Real-time per-field validation with range checks and engineering warnings |

---

## Quick Start

```bash
# 1. Enter project directory
cd jazib_helical-gear

# 2. Create and activate virtual environment (recommended)
python -m venv venv
source venv/bin/activate          # macOS / Linux
venv\Scripts\activate             # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
python app.py

# 5. Open in browser
#    http://127.0.0.1:5000
```

---

## Project Structure

```
jazib_helical-gear/
├── app.py                        # Flask routes + export endpoints
├── requirements.txt
├── README.md
├── calculations/
│   ├── __init__.py
│   └── gear_calculator.py        # Pure calculation engine (no Flask dependency)
├── static/
│   ├── css/
│   │   └── style.css             # Full custom dark-theme stylesheet
│   └── js/
│       └── main.js               # Frontend logic (validation, fetch, charts)
└── templates/
    └── index.html                # Single-page dashboard
```

---

## Input Parameters

| # | Parameter | Symbol | Unit | Range |
|---|---|---|---|---|
| 1 | Pitch Diameter | PD | in | 0.1 – 200 |
| 2 | Number of Teeth | Z | — | 6 – 500 |
| 3 | Helix Angle | β | ° | 1 – 89 |
| 4 | Normal Pressure Angle | φ | ° | 1 – 45 |
| 5 | Face Width | F | in | 0.01 – 100 |
| 6 | Input Power | HP | HP | 0.001 – 100,000 |
| 7 | Rotational Speed | — | RPM | 1 – 100,000 |
| 8 | Pinion Teeth | Z₁ | — | 6 – 500 |
| 9 | Gear Teeth | Z₂ | — | 6 – 500 |
| 10 | Service Factor | Ks | — | 0.5 – 5 |

---

## Output Parameters

| # | Parameter | Formula |
|---|---|---|
| 1 | Diametral Pitch (DP) | Z / PD |
| 2 | Circular Pitch (CP) | π / DP |
| 3 | Base Circle Diameter | PD · cos(φₜ) |
| 4 | Outside Diameter | PD + 2/DP |
| 5 | Root Diameter | PD − 2.5/DP |
| 6 | Lead | π · PD / tan(β) |
| 7 | Gear Ratio | Z₂ / Z₁ |
| 8 | Tangential Force | (2T / PD) · Ks |
| 9 | Axial Force | Wₜ · tan(β) |
| 10 | Torque | HP × 63,025 / RPM |

> **Note:** `tan(φₜ) = tan(φₙ) / cos(β)` — transverse pressure angle is derived internally from the normal pressure angle input.

---

## Sample Input Values

```
Pitch Diameter (PD)   :  4.0   in
Number of Teeth (Z)   :  20
Helix Angle (β)       :  20.0  °
Pressure Angle (φ)    :  20.0  °
Face Width (F)        :  2.0   in
Input Power           :  10.0  HP
Rotational Speed      :  1750  RPM
Pinion Teeth (Z₁)     :  18
Gear Teeth (Z₂)       :  54
Service Factor (Ks)   :  1.25
```

Expected key results:

| Parameter | Value |
|---|---|
| Diametral Pitch | 5.0 teeth/in |
| Circular Pitch | 0.6283 in |
| Torque | 360.14 lb·in |
| Tangential Force | 225.09 lbf |
| Gear Ratio | 3.0 |

---

## Technology Stack

- **Backend:** Python 3.10+, Flask 3
- **Calculation Engine:** Pure Python (`math` stdlib only)
- **PDF Export:** ReportLab
- **Excel Export:** openpyxl
- **Frontend:** HTML5, CSS3 (custom), vanilla JavaScript (ES2020)
- **Charts:** Chart.js 4
- **Tooltips:** Tippy.js 6
- **Fonts:** Google Fonts (Inter + JetBrains Mono)

---

## Customisation Guide

- **Add a new output:** Add an entry to `OUTPUT_DEFS` in `main.js` and implement the corresponding block in `gear_calculator.py → calculate_gears()`.
- **Change colour scheme:** All colours are CSS custom properties in `:root {}` at the top of `style.css`.
- **Add a new input:** Add the field to `index.html`, register it in `INPUT_RULES` in `main.js`, and add parsing in `validate_inputs()` in `gear_calculator.py`.
- **Change calculation method:** All formulas are isolated in `calculations/gear_calculator.py` — no frontend changes required.
