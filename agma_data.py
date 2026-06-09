"""
AGMA Standard Values, Tables, and Reference Data
Imperial Units
"""

# Standard diametral pitches (normal, in⁻¹)
STANDARD_DIAMETRAL_PITCHES = [1, 1.25, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 64, 96, 120]

# Standard helix angles
STANDARD_HELIX_ANGLES = [15, 20, 23, 25, 30, 35, 45]

# Standard pressure angles
STANDARD_PRESSURE_ANGLES = [14.5, 20, 25]

# Quality Numbers
QUALITY_NUMBERS = {
    3: "Very rough",
    6: "Commercial quality",
    7: "Commercial quality (better)",
    9: "Precision",
    11: "Precision (high)",
    12: "Extra precision",
    13: "Very high precision",
}

# Elastic Coefficient Cp (sqrt(psi))
ELASTIC_COEFFICIENT = {
    ("steel", "steel"): 2300,
    ("steel", "cast_iron"): 2160,
    ("steel", "bronze"): 2160,
    ("cast_iron", "cast_iron"): 1960,
    ("cast_iron", "bronze"): 1950,
    ("bronze", "bronze"): 1850,
    ("steel", "aluminum"): 2090,
    ("aluminum", "aluminum"): 1930,
}

# Overload Factor Ko (Table 9-5)
Ko_TABLE = {
    ("uniform", "uniform"): 1.00,
    ("uniform", "light_shock"): 1.25,
    ("uniform", "moderate_shock"): 1.50,
    ("light_shock", "uniform"): 1.10,
    ("light_shock", "light_shock"): 1.35,
    ("light_shock", "moderate_shock"): 1.60,
    ("moderate_shock", "uniform"): 1.25,
    ("moderate_shock", "light_shock"): 1.50,
    ("moderate_shock", "heavy_shock"): 1.75,
    ("heavy_shock", "uniform"): 1.50,
    ("heavy_shock", "light_shock"): 1.75,
    ("heavy_shock", "heavy_shock"): 2.00,
}

# Reliability Factor Kr (Table 9-11)
Kr_TABLE = {
    0.90: 0.85,
    0.99: 1.00,
    0.999: 1.25,
    0.9999: 1.50,
}

# Temperature Factor Kt
Kt_VALUES = {
    "T <= 250F": 1.00,
    "250F < T <= 350F": 1.05,
    "T > 350F": "Calculate",
}

# Material allowable stresses (Table 9-9, 9-10) - psi
MATERIAL_DATA = {
    "steel_grade1_160HB": {
        "sat": 25000, "sac": 85000, "HB": 160,
        "description": "Steel Grade 1, 160 HB",
        "su": 80000, "sy": 60000
    },
    "steel_grade1_200HB": {
        "sat": 31000, "sac": 93000, "HB": 200,
        "description": "Steel Grade 1, 200 HB",
        "su": 100000, "sy": 80000
    },
    "steel_grade1_240HB": {
        "sat": 36000, "sac": 102000, "HB": 240,
        "description": "Steel Grade 1, 240 HB (through-hardened)",
        "su": 120000, "sy": 100000
    },
    "steel_grade1_300HB": {
        "sat": 44000, "sac": 116000, "HB": 300,
        "description": "Steel Grade 1, 300 HB",
        "su": 150000, "sy": 130000
    },
    "steel_grade1_360HB": {
        "sat": 52000, "sac": 131000, "HB": 360,
        "description": "Steel Grade 1, 360 HB",
        "su": 180000, "sy": 160000
    },
    "steel_grade2_160HB": {
        "sat": 32000, "sac": 95000, "HB": 160,
        "description": "Steel Grade 2, 160 HB",
        "su": 80000, "sy": 60000
    },
    "steel_grade2_200HB": {
        "sat": 38000, "sac": 105000, "HB": 200,
        "description": "Steel Grade 2, 200 HB",
        "su": 100000, "sy": 80000
    },
    "steel_grade2_240HB": {
        "sat": 44000, "sac": 114000, "HB": 240,
        "description": "Steel Grade 2, 240 HB",
        "su": 120000, "sy": 100000
    },
    "steel_grade2_300HB": {
        "sat": 54000, "sac": 131000, "HB": 300,
        "description": "Steel Grade 2, 300 HB",
        "su": 150000, "sy": 130000
    },
    "steel_grade3_case_carb": {
        "sat": 65000, "sac": 170000, "HB": 58,
        "description": "Steel Grade 3, Case Carburized & Hardened",
        "su": 200000, "sy": 160000
    },
    "steel_nitrided_83.5HRA": {
        "sat": 55000, "sac": 150000, "HB": 250,
        "description": "Steel, Nitrided 83.5 HRA",
        "su": 150000, "sy": 130000
    },
    "cast_iron_class30": {
        "sat": 8500, "sac": 65000, "HB": 174,
        "description": "Gray Cast Iron ASTM A48 Class 30",
        "su": 30000, "sy": 0
    },
    "cast_iron_class40": {
        "sat": 13000, "sac": 75000, "HB": 201,
        "description": "Gray Cast Iron ASTM A48 Class 40",
        "su": 40000, "sy": 0
    },
    "ductile_iron_60_40_18": {
        "sat": 22000, "sac": 77000, "HB": 140,
        "description": "Ductile Iron ASTM A536 60-40-18 Annealed",
        "su": 60000, "sy": 40000
    },
    "ductile_iron_80_55_06": {
        "sat": 22000, "sac": 77000, "HB": 179,
        "description": "Ductile Iron ASTM A536 80-55-06 Q&T",
        "su": 80000, "sy": 55000
    },
    "ductile_iron_100_70_03": {
        "sat": 27000, "sac": 92000, "HB": 229,
        "description": "Ductile Iron ASTM A536 100-70-03 Q&T",
        "su": 100000, "sy": 70000
    },
    "bronze_sand_cast": {
        "sat": 5700, "sac": 30000, "HB": 60,
        "description": "Bronze Sand Cast (su=40 ksi)",
        "su": 40000, "sy": 20000
    },
    "bronze_heat_treated": {
        "sat": 23600, "sac": 65000, "HB": 100,
        "description": "Bronze Heat Treated (su=90 ksi)",
        "su": 90000, "sy": 60000
    },
}

# Design life recommendations (hours)
DESIGN_LIFE = {
    "domestic_appliances": (1000, 2000),
    "aircraft_engines": (1000, 4000),
    "automotive": (1500, 5000),
    "agricultural": (3000, 6000),
    "elevators_industrial_fans": (8000, 15000),
    "electric_motors_industrial": (20000, 30000),
    "pumps_compressors": (40000, 60000),
    "critical_24h_operation": (100000, 200000),
}

# Rim Thickness Factor Kb
Kb_TABLE = {
    "solid_gear": 1.0,
    "thin_rim_1.2": 1.6,
    "thin_rim_1.0": 2.0,
}

# Default/standard AGMA values
AGMA_DEFAULTS = {
    "Ko": 1.25,
    "KT": 1.00,
    "KR": 1.00,
    "Kb": 1.00,
    "Cf": 1.00,
    "CH": 1.00,
    "Qv": 6,
    "phi_n": 20.0,
    "psi": 20.0,
    "SF": 1.0,
    "face_width_factor_low": 10.0,
    "face_width_factor_high": 12.0,
}


def get_standard_Cp(pinion_material, gear_material):
    """Return standard elastic coefficient Cp"""
    key = (pinion_material, gear_material)
    if key in ELASTIC_COEFFICIENT:
        return ELASTIC_COEFFICIENT[key]
    key_rev = (gear_material, pinion_material)
    if key_rev in ELASTIC_COEFFICIENT:
        return ELASTIC_COEFFICIENT[key_rev]
    return 2300  # default steel-steel


def get_material_properties(material_key):
    """Return material properties dict"""
    return MATERIAL_DATA.get(material_key, None)


def get_Kr(reliability):
    """Return Kr for given reliability level"""
    for r, kr in sorted(Kr_TABLE.items()):
        if reliability <= r:
            return kr
    return 1.50


def calc_sat_from_HB(HB, grade=1):
    """
    Allowable bending stress from HB (through-hardened steel)
    Grade 1: sat = (0.533*HB + 88.3) ksi
    Grade 2: sat = (0.703*HB + 113) ksi
    """
    if grade == 1:
        return (0.533 * HB + 88.3) * 1000
    else:
        return (0.703 * HB + 113.0) * 1000


def calc_sac_from_HB(HB, grade=1):
    """
    Allowable contact stress from HB (through-hardened steel)
    Grade 1: sac = 322*HB + 29100 psi
    Grade 2: sac = 363*HB + 29560 psi
    """
    if grade == 1:
        return 322 * HB + 29100
    else:
        return 363 * HB + 29560
