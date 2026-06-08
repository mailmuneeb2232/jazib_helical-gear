"""
Helical Gear Calculation Engine
All calculations are PD-based using inch units.
"""

import math


def calculate_gears(inputs: dict, selected_outputs: list) -> dict:
    """
    Main calculation function.
    inputs: dict of validated input values
    selected_outputs: list of output keys to calculate
    Returns dict of results and any warnings.
    """
    PD = inputs["pitch_diameter"]       # inches
    Z  = inputs["num_teeth"]            # count
    beta_deg = inputs["helix_angle"]    # degrees
    phi_n_deg = inputs["pressure_angle"]# normal pressure angle, degrees
    F  = inputs["face_width"]           # inches
    HP = inputs["power"]                # horsepower
    RPM = inputs["rpm"]
    Z1 = inputs["pinion_teeth"]
    Z2 = inputs["gear_teeth"]
    Ks = inputs["service_factor"]

    beta = math.radians(beta_deg)
    phi_n = math.radians(phi_n_deg)

    # Transverse pressure angle (for helical gears)
    tan_phi_t = math.tan(phi_n) / math.cos(beta)
    phi_t = math.atan(tan_phi_t)

    # Diametral pitch (teeth per inch)
    DP = Z / PD

    # Normal diametral pitch
    DP_n = DP / math.cos(beta)

    warnings = []
    results = {}

    # --- Validation warnings ---
    if F < PD * 0.5:
        warnings.append("Face width is less than 0.5 × PD — may be too narrow for load sharing.")
    if F > PD * 2.0:
        warnings.append("Face width exceeds 2 × PD — may cause uneven load distribution.")
    if beta_deg < 5:
        warnings.append("Helix angle below 5° provides minimal helical benefit.")
    if beta_deg > 45:
        warnings.append("Helix angle above 45° produces high axial thrust — verify bearing capacity.")
    if DP < 0.5:
        warnings.append("Diametral pitch below 0.5 — very coarse gear; verify application suitability.")

    # --- Selected output calculations ---

    if "diametral_pitch" in selected_outputs:
        results["diametral_pitch"] = {
            "label": "Diametral Pitch (DP)",
            "value": round(DP, 4),
            "unit": "teeth/in",
            "formula": "DP = Z / PD",
            "description": "Number of teeth per inch of pitch diameter."
        }

    if "circular_pitch" in selected_outputs:
        CP = math.pi / DP
        results["circular_pitch"] = {
            "label": "Circular Pitch (CP)",
            "value": round(CP, 6),
            "unit": "in",
            "formula": "CP = π / DP = π × PD / Z",
            "description": "Arc distance between corresponding points of adjacent teeth."
        }

    if "base_circle_diameter" in selected_outputs:
        BCD = PD * math.cos(phi_t)
        results["base_circle_diameter"] = {
            "label": "Base Circle Diameter",
            "value": round(BCD, 6),
            "unit": "in",
            "formula": "BCD = PD × cos(φₜ),  tan(φₜ) = tan(φₙ) / cos(β)",
            "description": "Diameter of the base circle from which the involute tooth profile is generated."
        }

    if "outside_diameter" in selected_outputs:
        OD = PD + 2.0 / DP
        results["outside_diameter"] = {
            "label": "Outside Diameter (OD)",
            "value": round(OD, 6),
            "unit": "in",
            "formula": "OD = PD + 2 / DP",
            "description": "Overall outer diameter of the gear (addendum = 1/DP)."
        }

    if "root_diameter" in selected_outputs:
        # Standard dedendum = 1.25 / DP
        RD = PD - 2.5 / DP
        results["root_diameter"] = {
            "label": "Root Diameter (RD)",
            "value": round(RD, 6),
            "unit": "in",
            "formula": "RD = PD − 2.5 / DP",
            "description": "Diameter at the base of the tooth space (dedendum = 1.25/DP)."
        }
        if RD <= 0:
            warnings.append("Root diameter is non-positive — gear geometry is invalid.")

    if "lead" in selected_outputs:
        if abs(math.tan(beta)) < 1e-9:
            lead_val = float("inf")
            warnings.append("Helix angle is 0° — lead is infinite (spur gear).")
        else:
            lead_val = math.pi * PD / math.tan(beta)
        results["lead"] = {
            "label": "Lead (L)",
            "value": round(lead_val, 6) if lead_val != float("inf") else "∞",
            "unit": "in",
            "formula": "L = π × PD / tan(β)",
            "description": "Axial distance for one complete revolution of the helix."
        }

    if "gear_ratio" in selected_outputs:
        GR = Z2 / Z1
        results["gear_ratio"] = {
            "label": "Gear Ratio (GR)",
            "value": round(GR, 4),
            "unit": "—",
            "formula": "GR = Z₂ / Z₁",
            "description": "Speed reduction ratio from pinion (Z₁) to gear (Z₂)."
        }

    if "tangential_force" in selected_outputs:
        # Torque on driving gear (lb-in)
        T = (HP * 63025.0) / RPM
        Wt = (2.0 * T / PD) * Ks
        results["tangential_force"] = {
            "label": "Tangential Force (Wₜ)",
            "value": round(Wt, 4),
            "unit": "lbf",
            "formula": "Wₜ = (2T / PD) × Ks,  T = HP × 63025 / RPM",
            "description": "Tangential component of the tooth load, scaled by service factor."
        }

    if "axial_force" in selected_outputs:
        T = (HP * 63025.0) / RPM
        Wt = (2.0 * T / PD) * Ks
        Wa = Wt * math.tan(beta)
        results["axial_force"] = {
            "label": "Axial Force (Wₐ)",
            "value": round(Wa, 4),
            "unit": "lbf",
            "formula": "Wₐ = Wₜ × tan(β)",
            "description": "Axial (thrust) component of the tooth load due to helix angle."
        }

    if "torque" in selected_outputs:
        T = (HP * 63025.0) / RPM
        results["torque"] = {
            "label": "Torque (T)",
            "value": round(T, 4),
            "unit": "lb·in",
            "formula": "T = HP × 63025 / RPM",
            "description": "Driving torque at the gear shaft."
        }

    return {"results": results, "warnings": warnings}


def validate_inputs(data: dict) -> tuple[dict, list]:
    """
    Parse and validate raw form inputs.
    Returns (parsed_values_dict, error_list).
    """
    errors = []
    parsed = {}

    def get_float(key, label, lo, hi):
        try:
            v = float(data.get(key, ""))
            if not (lo <= v <= hi):
                errors.append(f"{label} must be between {lo} and {hi}.")
            return v
        except (ValueError, TypeError):
            errors.append(f"{label} must be a valid number.")
            return None

    def get_int(key, label, lo, hi):
        try:
            v = int(float(data.get(key, "")))
            if not (lo <= v <= hi):
                errors.append(f"{label} must be between {lo} and {hi}.")
            return v
        except (ValueError, TypeError):
            errors.append(f"{label} must be a valid integer.")
            return None

    parsed["pitch_diameter"]  = get_float("pitch_diameter",  "Pitch Diameter (PD)",   0.1, 200.0)
    parsed["num_teeth"]       = get_int(  "num_teeth",        "Number of Teeth (Z)",   6,   500)
    parsed["helix_angle"]     = get_float("helix_angle",      "Helix Angle (β)",        1,   89.0)
    parsed["pressure_angle"]  = get_float("pressure_angle",   "Pressure Angle (φ)",     1,   45.0)
    parsed["face_width"]      = get_float("face_width",       "Face Width (F)",          0.01, 100.0)
    parsed["power"]           = get_float("power",            "Input Power (HP)",        0.001, 100000.0)
    parsed["rpm"]             = get_float("rpm",              "Rotational Speed (RPM)", 1,   100000.0)
    parsed["pinion_teeth"]    = get_int(  "pinion_teeth",     "Pinion Teeth (Z₁)",      6,   500)
    parsed["gear_teeth"]      = get_int(  "gear_teeth",       "Gear Teeth (Z₂)",        6,   500)
    parsed["service_factor"]  = get_float("service_factor",   "Service Factor (Ks)",    0.5, 5.0)

    # Remove None values so calc function doesn't crash
    parsed = {k: v for k, v in parsed.items() if v is not None}
    return parsed, errors
