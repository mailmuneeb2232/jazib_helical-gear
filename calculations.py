"""
AGMA Helical Gear Design Calculations - Imperial Units
"""
import math
from typing import Dict, Optional, Tuple, List

class HelicalGearCalculations:

    # GEOMETRY CALCULATIONS

    @staticmethod
    def calc_gear_ratio(Np, Ng):
        """mG = Ng / Np"""
        return Ng / Np, "mG = Ng / Np", f"mG = {Ng} / {Np}", "dimensionless"

    @staticmethod
    def calc_Pt_from_Pn_psi(Pn, psi):
        """Pt = Pn * cos(psi)"""
        psi_r = math.radians(psi)
        result = Pn * math.cos(psi_r)
        return result, "Pt = Pn × cos(ψ)", f"Pt = {Pn} × cos({psi}°)", "in⁻¹"

    @staticmethod
    def calc_Pn_from_Pt_psi(Pt, psi):
        """Pn = Pt / cos(psi)"""
        psi_r = math.radians(psi)
        result = Pt / math.cos(psi_r)
        return result, "Pn = Pt / cos(ψ)", f"Pn = {Pt} / cos({psi}°)", "in⁻¹"

    @staticmethod
    def calc_phi_t(phi_n, psi):
        """tan(phi_t) = tan(phi_n) / cos(psi)"""
        phi_n_r = math.radians(phi_n)
        psi_r = math.radians(psi)
        result = math.degrees(math.atan(math.tan(phi_n_r) / math.cos(psi_r)))
        return result, "φt = arctan(tan(φn) / cos(ψ))", f"φt = arctan(tan({phi_n}°) / cos({psi}°))", "degrees"

    @staticmethod
    def calc_Dp(Np, Pt):
        """Dp = Np / Pt"""
        result = Np / Pt
        return result, "Dp = Np / Pt", f"Dp = {Np} / {Pt:.4f}", "in"

    @staticmethod
    def calc_Dg(Ng, Pt):
        """Dg = Ng / Pt"""
        result = Ng / Pt
        return result, "Dg = Ng / Pt", f"Dg = {Ng} / {Pt:.4f}", "in"

    @staticmethod
    def calc_center_distance(Dp, Dg):
        """C = (Dp + Dg) / 2"""
        result = (Dp + Dg) / 2.0
        return result, "C = (Dp + Dg) / 2", f"C = ({Dp:.4f} + {Dg:.4f}) / 2", "in"

    @staticmethod
    def calc_addendum(Pn):
        """a = 1 / Pn"""
        result = 1.0 / Pn
        return result, "a = 1 / Pn", f"a = 1 / {Pn}", "in"

    @staticmethod
    def calc_dedendum(Pn):
        """b = 1.25 / Pn"""
        result = 1.25 / Pn
        return result, "b = 1.25 / Pn", f"b = 1.25 / {Pn}", "in"

    @staticmethod
    def calc_normal_circular_pitch(Pn):
        """pn = pi / Pn"""
        result = math.pi / Pn
        return result, "pn = π / Pn", f"pn = π / {Pn}", "in"

    @staticmethod
    def calc_transverse_circular_pitch(Pt):
        """pt = pi / Pt"""
        result = math.pi / Pt
        return result, "pt = π / Pt", f"pt = π / {Pt:.4f}", "in"

    @staticmethod
    def calc_base_diameter(D, phi_t):
        """Db = D * cos(phi_t)"""
        phi_t_r = math.radians(phi_t)
        result = D * math.cos(phi_t_r)
        return result, "Db = D × cos(φt)", f"Db = {D:.4f} × cos({phi_t:.4f}°)", "in"

    @staticmethod
    def calc_normal_module(Pn):
        """mn = 25.4 / Pn"""
        result = 25.4 / Pn
        return result, "mn = 25.4 / Pn", f"mn = 25.4 / {Pn}", "mm"

    @staticmethod
    def calc_transverse_module(Pt):
        """mt = 25.4 / Pt"""
        result = 25.4 / Pt
        return result, "mt = 25.4 / Pt", f"mt = 25.4 / {Pt:.4f}", "mm"

    @staticmethod
    def calc_Np_from_Dp_Pt(Dp, Pt):
        """Np = Dp * Pt"""
        result = Dp * Pt
        return round(result), "Np = Dp × Pt", f"Np = {Dp:.4f} × {Pt:.4f}", "teeth"

    @staticmethod
    def calc_Ng_from_Dg_Pt(Dg, Pt):
        """Ng = Dg * Pt"""
        result = Dg * Pt
        return round(result), "Ng = Dg × Pt", f"Ng = {Dg:.4f} × {Pt:.4f}", "teeth"

    @staticmethod
    def calc_Ng_from_mG_Np(mG, Np):
        """Ng = mG * Np"""
        result = mG * Np
        return round(result), "Ng = mG × Np", f"Ng = {mG:.4f} × {Np}", "teeth"

    # FORCE ANALYSIS

    @staticmethod
    def calc_pitch_line_velocity(Dp, N):
        """V = pi * Dp * N / 12  (ft/min)"""
        result = math.pi * Dp * N / 12.0
        return result, "V = π × Dp × N / 12", f"V = π × {Dp:.4f} × {N} / 12", "ft/min"

    @staticmethod
    def calc_tangential_force(HP, V):
        """Ft = 33000 * HP / V  (lbf)"""
        result = 33000.0 * HP / V
        return result, "Ft = 33,000 × HP / V", f"Ft = 33,000 × {HP} / {V:.2f}", "lbf"

    @staticmethod
    def calc_radial_force(Ft, phi_t):
        """Fr = Ft * tan(phi_t)"""
        phi_t_r = math.radians(phi_t)
        result = Ft * math.tan(phi_t_r)
        return result, "Fr = Ft × tan(φt)", f"Fr = {Ft:.2f} × tan({phi_t:.4f}°)", "lbf"

    @staticmethod
    def calc_axial_force(Ft, psi):
        """Fa = Ft * tan(psi)"""
        psi_r = math.radians(psi)
        result = Ft * math.tan(psi_r)
        return result, "Fa = Ft × tan(ψ)", f"Fa = {Ft:.2f} × tan({psi}°)", "lbf"

    @staticmethod
    def calc_torque(HP, N):
        """T = 63025 * HP / N  (lb·in)"""
        result = 63025.0 * HP / N
        return result, "T = 63,025 × HP / N", f"T = 63,025 × {HP} / {N}", "lb·in"

    # AGMA DYNAMIC FACTOR Kv
    @staticmethod
    def calc_Kv(V, Qv):
        """
        AGMA Dynamic Factor
        B = 0.25*(12-Qv)^(2/3)
        A = 50 + 56*(1-B)
        Kv = ((A + sqrt(V))/A)^B
        """
        B = 0.25 * (12 - Qv) ** (2.0 / 3.0)
        A = 50 + 56 * (1 - B)
        result = ((A + math.sqrt(V)) / A) ** B
        formula = "Kv = ((A + √V) / A)^B\nwhere B = 0.25×(12-Qv)^(2/3), A = 50+56×(1-B)"
        substitution = f"B = {B:.4f}, A = {A:.4f}\nKv = (({A:.4f} + √{V:.2f}) / {A:.4f})^{B:.4f}"
        return result, formula, substitution, "dimensionless"

    # AGMA SIZE FACTOR Ks
    @staticmethod
    def calc_Ks(Pn, F, J):
        """
        Ks = 1.192 * (F * sqrt(Y) / Pn)^0.0535   AGMA
        where Y ≈ J for simplification
        For Pn >= 5: Ks = 1.0
        """
        if Pn >= 5:
            return 1.0, "Ks = 1.0 (for Pn ≥ 5)", f"Ks = 1.0 (Pn = {Pn} ≥ 5)", "dimensionless"
        result = 1.192 * (F * math.sqrt(J) / Pn) ** 0.0535
        result = max(1.0, result)
        formula = "Ks = 1.192 × (F × √J / Pn)^0.0535"
        substitution = f"Ks = 1.192 × ({F} × √{J} / {Pn})^0.0535"
        return result, formula, substitution, "dimensionless"

    # AGMA LOAD DISTRIBUTION FACTOR Km (simplified)
    @staticmethod
    def calc_Km(F, Dp):
        """
        Simplified AGMA Km
        Km = 1 + Cpf + Cma
        Cpf = F/(10*Dp) - 0.025  for F <= 1
        Cpf = F/(10*Dp) - 0.0375 + 0.0125*F  for 1 < F <= 17
        Cma from face width
        """
        # Cpf calculation
        if F <= 1.0:
            Cpf = F / (10.0 * Dp) - 0.025
        elif F <= 17.0:
            Cpf = F / (10.0 * Dp) - 0.0375 + 0.0125 * F
        else:
            Cpf = F / (10.0 * Dp) - 0.1109 + 0.0207 * F - 0.000228 * F ** 2
        Cpf = max(0, Cpf)

        # Cma (commercial enclosed gear units)
        if F <= 1.0:
            Cma = 0.0675 + 0.0128 * F - 0.926e-3 * F ** 2
        elif F <= 6.0:
            Cma = 0.0675 + 0.0128 * F - 0.926e-4 * F ** 2
        elif F <= 10.0:
            Cma = 0.00360 + 0.0102 * F - 0.822e-4 * F ** 2
        else:
            Cma = 0.00360 + 0.0102 * F - 0.822e-4 * F ** 2

        Cpm = 1.0  # assume straddle mounting
        Ce = 1.0   # assumed
        Cmc = 1.0  # uncrowned teeth

        Km = 1 + Cmc * (Cpf * Cpm + Cma * Ce)
        formula = "Km = 1 + Cmc×(Cpf×Cpm + Cma×Ce)"
        substitution = f"Km = 1 + {Cmc}×({Cpf:.4f}×{Cpm} + {Cma:.4f}×{Ce})"
        return Km, formula, substitution, "dimensionless"

    # STRESS CALCULATIONS
    @staticmethod
    def calc_bending_stress(Ft, Pn, F, J, Ko, Kv, Ks, Km, Kb):
        """
        AGMA Bending Stress
        sigma_t = Ft * Pn / (F * J) * Ko * Kv * Ks * Km * Kb
        """
        result = (Ft * Pn / (F * J)) * Ko * Kv * Ks * Km * Kb
        formula = "σt = (Ft × Pn / (F × J)) × Ko × Kv × Ks × Km × Kb"
        substitution = (f"σt = ({Ft:.2f} × {Pn} / ({F} × {J})) "
                       f"× {Ko} × {Kv:.4f} × {Ks:.4f} × {Km:.4f} × {Kb}")
        return result, formula, substitution, "psi"

    @staticmethod
    def calc_contact_stress(Cp, Ft, Ko, Kv, Ks, Dp, F, I, Km, Cf=1.0):
        """
        AGMA Contact Stress
        sigma_c = Cp * sqrt(Ft*Ko*Kv*Ks/(Dp*F) * Km*Cf/I)
        """
        inner = (Ft * Ko * Kv * Ks / (Dp * F)) * (Km * Cf / I)
        result = Cp * math.sqrt(inner)
        formula = "σc = Cp × √(Ft×Ko×Kv×Ks×Km×Cf / (Dp×F×I))"
        substitution = (f"σc = {Cp} × √({Ft:.2f}×{Ko}×{Kv:.4f}×{Ks:.4f}×{Km:.4f}×{Cf} "
                       f"/ ({Dp:.4f}×{F}×{I}))")
        return result, formula, substitution, "psi"

    @staticmethod
    def calc_allowable_bending_stress(sat, YN, KT, KR, SF=1.0):
        """
        sigma_at = sat * YN / (SF * KT * KR)
        """
        result = sat * YN / (SF * KT * KR)
        formula = "σat = sat × YN / (SF × KT × KR)"
        substitution = f"σat = {sat} × {YN:.4f} / ({SF} × {KT} × {KR})"
        return result, formula, substitution, "psi"

    @staticmethod
    def calc_allowable_contact_stress(sac, ZN, CH, KT, KR, SF=1.0):
        """
        sigma_ac = sac * ZN * CH / (SF * KT * KR)
        """
        result = sac * ZN * CH / (SF * KT * KR)
        formula = "σac = sac × ZN × CH / (SF × KT × KR)"
        substitution = f"σac = {sac} × {ZN:.4f} × {CH} / ({SF} × {KT} × {KR})"
        return result, formula, substitution, "psi"

    @staticmethod
    def calc_bending_safety_factor(sigma_at, sigma_t):
        """SFb = sigma_at / sigma_t"""
        result = sigma_at / sigma_t
        formula = "SFb = σat / σt"
        substitution = f"SFb = {sigma_at:.2f} / {sigma_t:.2f}"
        return result, formula, substitution, "dimensionless"

    @staticmethod
    def calc_contact_safety_factor(sigma_ac, sigma_c):
        """SFc = sigma_ac / sigma_c"""
        result = sigma_ac / sigma_c
        formula = "SFc = σac / σc"
        substitution = f"SFc = {sigma_ac:.2f} / {sigma_c:.2f}"
        return result, formula, substitution, "dimensionless"

    # STRESS CYCLE FACTORS
    @staticmethod
    def calc_YN(Nc, hardness_type="160HB"):
        """Bending Stress Cycle Factor YN"""
        if hardness_type == "160HB":
            result = 1.3558 * Nc ** (-0.0178)
        elif hardness_type == "250HB":
            result = 1.3558 * Nc ** (-0.0178)
        elif hardness_type == "400HB":
            result = 9.4518 * Nc ** (-0.148)
        elif hardness_type == "case_carb":
            result = 6.1514 * Nc ** (-0.1192)
        elif hardness_type == "nitrided":
            result = 3.517 * Nc ** (-0.0817)
        else:
            result = 1.3558 * Nc ** (-0.0178)
        formula = "YN = C × Nc^(-n)  [from AGMA Fig 9-21]"
        substitution = f"YN = f(Nc={Nc:.3e}, material={hardness_type})"
        return result, formula, substitution, "dimensionless"

    @staticmethod
    def calc_ZN(Nc, hardness_type="std"):
        """Contact Stress Cycle Factor ZN"""
        if hardness_type == "nitrided":
            result = 1.249 * Nc ** (-0.0138)
        elif hardness_type == "case_carb":
            result = 2.466 * Nc ** (-0.056)
        else:
            result = 1.4488 * Nc ** (-0.023)
        formula = "ZN = C × Nc^(-n)  [from AGMA Fig 9-22]"
        substitution = f"ZN = f(Nc={Nc:.3e}, material={hardness_type})"
        return result, formula, substitution, "dimensionless"

    @staticmethod
    def calc_load_cycles(L, n, q=1):
        """Nc = 60 * L * n * q"""
        result = 60.0 * L * n * q
        formula = "Nc = 60 × L × n × q"
        substitution = f"Nc = 60 × {L} × {n} × {q}"
        return result, formula, substitution, "cycles"

    # GEOMETRY FACTOR I (Contact) for helical gears
    @staticmethod
    def calc_I_factor(phi_t, psi, mG):
        """
        Geometry Factor I (Pitting Resistance) for helical gears
        I = (cos(phi_t) * sin(phi_t)) / (2 * mN) * (mG / (mG + 1))
        """
        phi_t_r = math.radians(phi_t)
        psi_r = math.radians(psi)
        # Load sharing ratio mN for helical gears
        psi_b = math.atan(math.tan(psi_r) * math.cos(phi_t_r))
        mN = 1.0 / math.cos(psi_b)

        I = (math.cos(phi_t_r) * math.sin(phi_t_r)) / (2.0 * mN) * (mG / (mG + 1.0))
        formula = "I = (cos(φt)×sin(φt)) / (2×mN) × (mG/(mG+1))"
        substitution = (f"ψb = arctan(tan({psi}°)×cos({phi_t:.4f}°)) = {math.degrees(psi_b):.4f}°\n"
                       f"mN = 1/cos(ψb) = {mN:.4f}\n"
                       f"I = (cos({phi_t:.4f}°)×sin({phi_t:.4f}°)) / (2×{mN:.4f}) × ({mG:.4f}/({mG:.4f}+1))")
        return I, formula, substitution, "dimensionless"

    # EFFICIENCY
    @staticmethod
    def calc_efficiency(psi, phi_n):
        """e = approximate efficiency for helical gear"""
        f = 0.05  # friction coefficient
        psi_r = math.radians(psi)
        e = (1 - math.pi * f / math.tan(psi_r)) * 100
        e = max(90.0, min(99.5, e))
        formula = "η ≈ (1 - π×f/tan(ψ)) × 100%"
        substitution = f"η = (1 - π×{f}/tan({psi}°)) × 100%"
        return e, formula, substitution, "%"

    @staticmethod
    def calc_face_width_from_Pn(Pn, factor=10.0):
        """F = factor / Pn  (AGMA: 10/Pn to 12/Pn)"""
        result = factor / Pn
        formula = f"F = {factor:.0f} / Pn"
        substitution = f"F = {factor:.0f} / {Pn}"
        return result, formula, substitution, "in"

    @staticmethod
    def calc_RPM_gear(RPM_pinion, mG):
        """N_gear = N_pinion / mG"""
        result = RPM_pinion / mG
        formula = "Ng_rpm = Np_rpm / mG"
        substitution = f"Ng_rpm = {RPM_pinion} / {mG:.4f}"
        return result, formula, substitution, "rpm"
