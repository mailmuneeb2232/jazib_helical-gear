"""
Helical Gear Design Software - Main Window
AGMA Standards - Imperial Units (Inch System)
"""
import sys
import json
import math
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QLineEdit, QPushButton, QScrollArea,
    QGroupBox, QRadioButton, QButtonGroup, QTabWidget, QTextEdit,
    QComboBox, QMessageBox, QFileDialog, QFrame, QSizePolicy,
    QCheckBox, QSplitter, QToolButton, QStatusBar, QSpacerItem
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QColor, QPalette, QTextDocument, QPainter
import gear_calculations as calc_module
import agma_data as agma
from report_generator import ReportGenerator

# ─────────────────────────────────────────────────────────────────
PARAMETERS = {
    "gear_ratio":    ("Gear Ratio (mG)",                           "dimensionless", "Geometry"),
    "Np":            ("Number of Teeth – Pinion (Np)",             "teeth",         "Geometry"),
    "Ng":            ("Number of Teeth – Gear (Ng)",               "teeth",         "Geometry"),
    "Pn":            ("Normal Diametral Pitch (Pn)",               "in⁻¹",          "Geometry"),
    "Pt":            ("Transverse Diametral Pitch (Pt)",           "in⁻¹",          "Geometry"),
    "phi_n":         ("Normal Pressure Angle (φn)",                "deg",           "Geometry"),
    "phi_t":         ("Transverse Pressure Angle (φt)",            "deg",           "Geometry"),
    "psi":           ("Helix Angle (ψ)",                           "deg",           "Geometry"),
    "Dp":            ("Pitch Diameter – Pinion (Dp)",              "in",            "Geometry"),
    "Dg":            ("Pitch Diameter – Gear (Dg)",                "in",            "Geometry"),
    "C":             ("Center Distance (C)",                       "in",            "Geometry"),
    "F":             ("Face Width (F)",                            "in",            "Geometry"),
    "addendum":      ("Addendum (a)",                              "in",            "Geometry"),
    "dedendum":      ("Dedendum (b)",                              "in",            "Geometry"),
    "normal_cp":     ("Normal Circular Pitch (pn)",                "in",            "Geometry"),
    "trans_cp":      ("Transverse Circular Pitch (pt)",            "in",            "Geometry"),
    "base_dia_p":    ("Base Diameter – Pinion (Dbp)",              "in",            "Geometry"),
    "base_dia_g":    ("Base Diameter – Gear (Dbg)",                "in",            "Geometry"),
    "normal_module": ("Normal Module (mn)",                        "mm",            "Geometry"),
    "trans_module":  ("Transverse Module (mt)",                    "mm",            "Geometry"),
    "HP":            ("Power (HP)",                                "hp",            "Power & Speed"),
    "N_pinion":      ("Pinion Speed (Np_rpm)",                     "rpm",           "Power & Speed"),
    "N_gear":        ("Gear Speed (Ng_rpm)",                       "rpm",           "Power & Speed"),
    "V":             ("Pitch Line Velocity (V)",                   "ft/min",        "Force Analysis"),
    "Ft":            ("Tangential Force (Ft)",                     "lbf",           "Force Analysis"),
    "Fr":            ("Radial Force (Fr)",                         "lbf",           "Force Analysis"),
    "Fa":            ("Axial/Thrust Force (Fa)",                   "lbf",           "Force Analysis"),
    "torque_p":      ("Torque – Pinion (Tp)",                      "lb·in",         "Force Analysis"),
    "Ko":            ("Overload Factor (Ko)",                      "–",             "AGMA Factors"),
    "Kv":            ("Dynamic Factor (Kv)",                       "–",             "AGMA Factors"),
    "Ks":            ("Size Factor (Ks)",                          "–",             "AGMA Factors"),
    "Km":            ("Load Distribution Factor (Km)",             "–",             "AGMA Factors"),
    "Kb":            ("Rim Thickness Factor (Kb)",                 "–",             "AGMA Factors"),
    "KR":            ("Reliability Factor (KR)",                   "–",             "AGMA Factors"),
    "KT":            ("Temperature Factor (KT)",                   "–",             "AGMA Factors"),
    "Cp":            ("Elastic Coefficient (Cp)",                  "√psi",          "AGMA Factors"),
    "J_factor":      ("Geometry Factor – Bending (J)",             "–",             "AGMA Factors"),
    "I_factor":      ("Geometry Factor – Contact (I)",             "–",             "AGMA Factors"),
    "Qv":            ("Quality Number (Qv)",                       "–",             "AGMA Factors"),
    "Cf":            ("Surface Condition Factor (Cf)",             "–",             "AGMA Factors"),
    "CH":            ("Hardness Ratio Factor (CH)",                "–",             "AGMA Factors"),
    "YN":            ("Bending Stress Cycle Factor (YN)",          "–",             "AGMA Factors"),
    "ZN":            ("Contact Stress Cycle Factor (ZN)",          "–",             "AGMA Factors"),
    "sigma_b":       ("Bending Stress (σt)",                       "psi",           "Stress Analysis"),
    "sigma_c":       ("Contact Stress (σc)",                       "psi",           "Stress Analysis"),
    "sigma_b_allow": ("Allowable Bending Stress (σat)",            "psi",           "Stress Analysis"),
    "sigma_c_allow": ("Allowable Contact Stress (σac)",            "psi",           "Stress Analysis"),
    "SF_b":          ("Bending Safety Factor (SFb)",               "–",             "Stress Analysis"),
    "SF_c":          ("Contact Safety Factor (SFc)",               "–",             "Stress Analysis"),
    "sat":           ("Allowable Bending Stress Number (sat)",     "psi",           "Material"),
    "sac":           ("Allowable Contact Stress Number (sac)",     "psi",           "Material"),
    "HB":            ("Brinell Hardness (HB)",                     "HB",            "Material"),
    "su":            ("Ultimate Tensile Strength (Su)",            "psi",           "Material"),
    "sy":            ("Yield Strength (Sy)",                       "psi",           "Material"),
    "Nc_p":          ("Load Cycles – Pinion (Nc)",                 "cycles",        "Design"),
    "efficiency":    ("Efficiency (η)",                            "%",             "Design"),
    "service_factor":("Service Factor (SF)",                       "–",             "Design"),
    "design_life":   ("Design Life (L)",                           "hours",         "Design"),
}

CATEGORIES = ["Geometry", "Power & Speed", "Force Analysis",
               "AGMA Factors", "Stress Analysis", "Material", "Design"]

# AGMA suggested/default values for inputs
AGMA_SUGGESTIONS = {
    "phi_n":        20.0,
    "psi":          20.0,
    "Ko":           1.25,
    "KT":           1.00,
    "KR":           1.00,
    "Kb":           1.00,
    "Cf":           1.00,
    "CH":           1.00,
    "Qv":           6,
    "J_factor":     0.36,
    "Cp":           2300,
    "service_factor": 1.0,
}

# ─── Dark / Light Stylesheets ─────────────────────────────────────
DARK_STYLE = """
QMainWindow, QWidget { background-color: #1e1e2e; color: #cdd6f4; }
QGroupBox { border: 1px solid #45475a; border-radius: 6px; margin-top: 10px;
            font-weight: bold; color: #89b4fa; padding: 8px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left;
                   padding: 0 6px; color: #89b4fa; }
QLineEdit { background-color: #313244; border: 1px solid #45475a; border-radius: 4px;
            color: #cdd6f4; padding: 4px 8px; min-height: 24px; }
QLineEdit:focus { border: 1px solid #89b4fa; }
QLineEdit:disabled { background-color: #1e1e2e; color: #6c7086; }
QPushButton { background-color: #313244; border: 1px solid #45475a; border-radius: 6px;
              color: #cdd6f4; padding: 6px 16px; min-height: 28px; }
QPushButton:hover { background-color: #45475a; }
QPushButton:pressed { background-color: #585b70; }
QPushButton#btn_calculate { background-color: #1e66f5; color: white; font-weight: bold;
                             border: none; font-size: 13px; min-height: 36px; border-radius: 8px; }
QPushButton#btn_calculate:hover { background-color: #2979f5; }
QPushButton#btn_agma { background-color: #40a02b; color: white; border: none; min-height: 22px;
                        padding: 2px 8px; font-size: 10px; border-radius: 4px; }
QPushButton#btn_agma:hover { background-color: #4ec337; }
QPushButton#btn_export_pdf { background-color: #d20f39; color: white; border: none; }
QPushButton#btn_export_excel { background-color: #179299; color: white; border: none; }
QPushButton#btn_clear { background-color: #e64553; color: white; border: none; }
QRadioButton { color: #cdd6f4; spacing: 5px; }
QRadioButton::indicator { width: 14px; height: 14px; }
QRadioButton::indicator:checked { background-color: #89b4fa; border: 2px solid #89b4fa; border-radius: 7px; }
QRadioButton::indicator:unchecked { background-color: #313244; border: 2px solid #45475a; border-radius: 7px; }
QTabWidget::pane { border: 1px solid #45475a; border-radius: 6px; }
QTabBar::tab { background-color: #313244; color: #cdd6f4; padding: 8px 16px; margin: 2px;
               border-radius: 4px; }
QTabBar::tab:selected { background-color: #89b4fa; color: #1e1e2e; font-weight: bold; }
QTextEdit { background-color: #181825; border: 1px solid #45475a; border-radius: 6px;
            color: #cdd6f4; font-family: 'Courier New', monospace; font-size: 12px; }
QScrollArea { border: none; }
QLabel#section_title { color: #89b4fa; font-size: 13px; font-weight: bold; }
QLabel#result_label { color: #a6e3a1; font-weight: bold; }
QLabel#error_label { color: #f38ba8; font-weight: bold; }
QLabel#warn_label { color: #fab387; font-weight: bold; }
QComboBox { background-color: #313244; border: 1px solid #45475a; color: #cdd6f4;
            padding: 4px 8px; border-radius: 4px; min-height: 24px; }
QComboBox QAbstractItemView { background-color: #313244; color: #cdd6f4; }
QStatusBar { background-color: #181825; color: #6c7086; }
QSplitter::handle { background-color: #45475a; }
QFrame#separator { background-color: #45475a; }
"""

LIGHT_STYLE = """
QMainWindow, QWidget { background-color: #eff1f5; color: #4c4f69; }
QGroupBox { border: 1px solid #bcc0cc; border-radius: 6px; margin-top: 10px;
            font-weight: bold; color: #1e66f5; padding: 8px; }
QGroupBox::title { subcontrol-origin: margin; subcontrol-position: top left;
                   padding: 0 6px; color: #1e66f5; }
QLineEdit { background-color: #ffffff; border: 1px solid #bcc0cc; border-radius: 4px;
            color: #4c4f69; padding: 4px 8px; min-height: 24px; }
QLineEdit:focus { border: 1px solid #1e66f5; }
QLineEdit:disabled { background-color: #e6e9ef; color: #acb0be; }
QPushButton { background-color: #e6e9ef; border: 1px solid #bcc0cc; border-radius: 6px;
              color: #4c4f69; padding: 6px 16px; min-height: 28px; }
QPushButton:hover { background-color: #dce0e8; }
QPushButton:pressed { background-color: #ccd0da; }
QPushButton#btn_calculate { background-color: #1e66f5; color: white; font-weight: bold;
                             border: none; font-size: 13px; min-height: 36px; border-radius: 8px; }
QPushButton#btn_calculate:hover { background-color: #0f5fe1; }
QPushButton#btn_agma { background-color: #40a02b; color: white; border: none; min-height: 22px;
                        padding: 2px 8px; font-size: 10px; border-radius: 4px; }
QPushButton#btn_export_pdf { background-color: #d20f39; color: white; border: none; }
QPushButton#btn_export_excel { background-color: #179299; color: white; border: none; }
QPushButton#btn_clear { background-color: #e64553; color: white; border: none; }
QRadioButton { color: #4c4f69; spacing: 5px; }
QRadioButton::indicator:checked { background-color: #1e66f5; border: 2px solid #1e66f5;
                                   border-radius: 7px; width:14px; height:14px; }
QRadioButton::indicator:unchecked { background-color: white; border: 2px solid #bcc0cc;
                                     border-radius: 7px; width:14px; height:14px; }
QTabWidget::pane { border: 1px solid #bcc0cc; border-radius: 6px; }
QTabBar::tab { background-color: #e6e9ef; color: #4c4f69; padding: 8px 16px; margin: 2px;
               border-radius: 4px; }
QTabBar::tab:selected { background-color: #1e66f5; color: white; font-weight: bold; }
QTextEdit { background-color: #ffffff; border: 1px solid #bcc0cc; border-radius: 6px;
            color: #4c4f69; font-family: 'Courier New', monospace; font-size: 12px; }
QScrollArea { border: none; }
QLabel#section_title { color: #1e66f5; font-size: 13px; font-weight: bold; }
QLabel#result_label { color: #40a02b; font-weight: bold; }
QLabel#error_label { color: #d20f39; font-weight: bold; }
QLabel#warn_label { color: #fe640b; font-weight: bold; }
QComboBox { background-color: #ffffff; border: 1px solid #bcc0cc; color: #4c4f69;
            padding: 4px 8px; border-radius: 4px; min-height: 24px; }
QStatusBar { background-color: #e6e9ef; color: #6c6f85; }
QFrame#separator { background-color: #bcc0cc; }
"""


# ─────────────────────────────────────────────────────────────────────────────
class ParameterRow(QWidget):
    """One row in the parameter list: label | Input/Output/None radios | value field | AGMA btn"""

    mode_changed = pyqtSignal(str, str)   # (param_id, mode)  mode = 'input'|'output'|'none'

    def __init__(self, param_id, label, unit, parent=None):
        super().__init__(parent)
        self.param_id = param_id
        self.label_text = label
        self.unit_text = unit

        layout = QHBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.setSpacing(6)

        # Label
        lbl = QLabel(f"{label} [{unit}]")
        lbl.setMinimumWidth(280)
        lbl.setWordWrap(True)
        layout.addWidget(lbl, 3)

        # Radio buttons
        self.rb_input  = QRadioButton("Input")
        self.rb_output = QRadioButton("Output")
        self.rb_none   = QRadioButton("–")
        self.rb_none.setChecked(True)

        self.btn_group = QButtonGroup(self)
        self.btn_group.addButton(self.rb_input,  0)
        self.btn_group.addButton(self.rb_output, 1)
        self.btn_group.addButton(self.rb_none,   2)

        rb_layout = QHBoxLayout()
        rb_layout.setSpacing(4)
        rb_layout.addWidget(self.rb_input)
        rb_layout.addWidget(self.rb_output)
        rb_layout.addWidget(self.rb_none)
        layout.addLayout(rb_layout, 2)

        # Value field
        self.value_edit = QLineEdit()
        self.value_edit.setPlaceholderText("value")
        self.value_edit.setEnabled(False)
        self.value_edit.setMinimumWidth(90)
        self.value_edit.setMaximumWidth(120)
        layout.addWidget(self.value_edit, 1)

        # Result label (shown when output is calculated)
        self.result_label = QLabel("")
        self.result_label.setObjectName("result_label")
        self.result_label.setMinimumWidth(120)
        layout.addWidget(self.result_label, 2)

        # AGMA suggestion button
        self.btn_agma = QPushButton("AGMA Default")
        self.btn_agma.setObjectName("btn_agma")
        self.btn_agma.setVisible(False)
        self.btn_agma.setMaximumWidth(100)
        self.btn_agma.clicked.connect(self._apply_agma_default)
        layout.addWidget(self.btn_agma, 1)

        # Connections
        self.rb_input.toggled.connect(self._on_mode_changed)
        self.rb_output.toggled.connect(self._on_mode_changed)
        self.rb_none.toggled.connect(self._on_mode_changed)

    def _on_mode_changed(self):
        mode = self.get_mode()
        self.value_edit.setEnabled(mode == 'input')
        # Show AGMA button only for inputs that have a suggestion and field is empty
        show_agma = (mode == 'input' and self.param_id in AGMA_SUGGESTIONS)
        self.btn_agma.setVisible(show_agma)
        if mode == 'output':
            self.result_label.setText("")
        self.mode_changed.emit(self.param_id, mode)

    def _apply_agma_default(self):
        if self.param_id in AGMA_SUGGESTIONS:
            self.value_edit.setText(str(AGMA_SUGGESTIONS[self.param_id]))

    def get_mode(self):
        if self.rb_input.isChecked():
            return 'input'
        elif self.rb_output.isChecked():
            return 'output'
        return 'none'

    def get_value(self):
        """Return float value or None"""
        txt = self.value_edit.text().strip()
        if not txt:
            return None
        try:
            return float(txt)
        except ValueError:
            return None

    def set_result(self, value, unit="", error=False, warning=False):
        if error:
            self.result_label.setObjectName("error_label")
            self.result_label.setText(str(value))
        elif warning:
            self.result_label.setObjectName("warn_label")
            self.result_label.setText(str(value))
        else:
            self.result_label.setObjectName("result_label")
            if isinstance(value, float):
                self.result_label.setText(f"{value:.4g} {unit}")
            else:
                self.result_label.setText(f"{value} {unit}")
        # Force stylesheet refresh
        self.result_label.style().unpolish(self.result_label)
        self.result_label.style().polish(self.result_label)

    def clear_result(self):
        self.result_label.setText("")

    def set_value(self, val):
        self.value_edit.setText(str(val))

    def reset(self):
        self.rb_none.setChecked(True)
        self.value_edit.clear()
        self.result_label.setText("")


# ─────────────────────────────────────────────────────────────────────────────
class CalculationEngine:
    """
    Resolves all selected outputs from available inputs.
    Uses a dependency-resolution approach with multiple formula paths.
    """

    def __init__(self):
        self.c = calc_module.HelicalGearCalculations()
        self.known = {}          # param_id -> float (inputs + intermediates)
        self.calc_details = {}   # param_id -> detail dict
        self.assumptions = {}    # param_id -> (label, value, unit, source)
        self.errors = {}         # param_id -> error message

    def reset(self, input_values: dict):
        self.known = dict(input_values)
        self.calc_details = {}
        self.assumptions = {}
        self.errors = {}

    def _store(self, pid, result, formula, subst, unit, label):
        self.known[pid] = result
        self.calc_details[pid] = {
            'label': label,
            'formula': formula,
            'substitution': subst,
            'result': result,
            'unit': unit,
        }

    def _assume(self, pid, value, unit, source="AGMA Default"):
        label = PARAMETERS[pid][0]
        self.known[pid] = value
        self.assumptions[pid] = (label, value, unit, source)

    def _has(self, *pids):
        return all(p in self.known and self.known[p] is not None for p in pids)

    # ── Geometry resolution helpers ──────────────────────────────
    def _resolve_psi(self):
        if not self._has('psi'):
            self._assume('psi', agma.AGMA_DEFAULTS['psi'], 'deg')

    def _resolve_phi_n(self):
        if not self._has('phi_n'):
            self._assume('phi_n', agma.AGMA_DEFAULTS['phi_n'], 'deg')

    def _resolve_Pn(self):
        if self._has('Pn'):
            return
        if self._has('Pt', 'psi'):
            r, f, s, u = self.c.calc_Pn_from_Pt_psi(self.known['Pt'], self.known['psi'])
            self._store('Pn', r, f, s, u, PARAMETERS['Pn'][0])

    def _resolve_Pt(self):
        if self._has('Pt'):
            return
        if self._has('Pn', 'psi'):
            r, f, s, u = self.c.calc_Pt_from_Pn_psi(self.known['Pn'], self.known['psi'])
            self._store('Pt', r, f, s, u, PARAMETERS['Pt'][0])

    def _resolve_phi_t(self):
        if self._has('phi_t'):
            return
        self._resolve_phi_n()
        self._resolve_psi()
        if self._has('phi_n', 'psi'):
            r, f, s, u = self.c.calc_phi_t(self.known['phi_n'], self.known['psi'])
            self._store('phi_t', r, f, s, u, PARAMETERS['phi_t'][0])

    def _resolve_Np(self):
        if self._has('Np'):
            return
        if self._has('Dp', 'Pt'):
            r, f, s, u = self.c.calc_Np_from_Dp_Pt(self.known['Dp'], self.known['Pt'])
            self._store('Np', r, f, s, u, PARAMETERS['Np'][0])
        elif self._has('gear_ratio', 'Ng'):
            r = round(self.known['Ng'] / self.known['gear_ratio'])
            self._store('Np', r, "Np = Ng / mG", f"Np = {self.known['Ng']} / {self.known['gear_ratio']:.4f}", "teeth", PARAMETERS['Np'][0])

    def _resolve_Ng(self):
        if self._has('Ng'):
            return
        if self._has('gear_ratio', 'Np'):
            r, f, s, u = self.c.calc_Ng_from_mG_Np(self.known['gear_ratio'], self.known['Np'])
            self._store('Ng', r, f, s, u, PARAMETERS['Ng'][0])
        elif self._has('Dg', 'Pt'):
            r, f, s, u = self.c.calc_Ng_from_Dg_Pt(self.known['Dg'], self.known['Pt'])
            self._store('Ng', r, f, s, u, PARAMETERS['Ng'][0])

    def _resolve_Dp(self):
        if self._has('Dp'):
            return
        self._resolve_Pt()
        if self._has('Np', 'Pt'):
            r, f, s, u = self.c.calc_Dp(self.known['Np'], self.known['Pt'])
            self._store('Dp', r, f, s, u, PARAMETERS['Dp'][0])

    def _resolve_Dg(self):
        if self._has('Dg'):
            return
        self._resolve_Pt()
        if self._has('Ng', 'Pt'):
            r, f, s, u = self.c.calc_Dg(self.known['Ng'], self.known['Pt'])
            self._store('Dg', r, f, s, u, PARAMETERS['Dg'][0])

    def _resolve_gear_ratio(self):
        if self._has('gear_ratio'):
            return
        if self._has('Np', 'Ng'):
            r, f, s, u = self.c.calc_gear_ratio(self.known['Np'], self.known['Ng'])
            self._store('gear_ratio', r, f, s, u, PARAMETERS['gear_ratio'][0])

    def _resolve_V(self):
        if self._has('V'):
            return
        self._resolve_Dp()
        if self._has('Dp', 'N_pinion'):
            r, f, s, u = self.c.calc_pitch_line_velocity(self.known['Dp'], self.known['N_pinion'])
            self._store('V', r, f, s, u, PARAMETERS['V'][0])

    def _resolve_Ft(self):
        if self._has('Ft'):
            return
        self._resolve_V()
        if self._has('HP', 'V'):
            r, f, s, u = self.c.calc_tangential_force(self.known['HP'], self.known['V'])
            self._store('Ft', r, f, s, u, PARAMETERS['Ft'][0])

    def _resolve_Kv(self):
        if self._has('Kv'):
            return
        self._resolve_V()
        if not self._has('Qv'):
            self._assume('Qv', agma.AGMA_DEFAULTS['Qv'], '–')
        if self._has('V', 'Qv'):
            r, f, s, u = self.c.calc_Kv(self.known['V'], self.known['Qv'])
            self._store('Kv', r, f, s, u, PARAMETERS['Kv'][0])

    def _resolve_Ks(self):
        if self._has('Ks'):
            return
        if not self._has('J_factor'):
            self._assume('J_factor', AGMA_SUGGESTIONS['J_factor'], '–')
        if self._has('Pn', 'F', 'J_factor'):
            r, f, s, u = self.c.calc_Ks(self.known['Pn'], self.known['F'], self.known['J_factor'])
            self._store('Ks', r, f, s, u, PARAMETERS['Ks'][0])

    def _resolve_Km(self):
        if self._has('Km'):
            return
        self._resolve_Dp()
        if self._has('F', 'Dp'):
            r, f, s, u = self.c.calc_Km(self.known['F'], self.known['Dp'])
            self._store('Km', r, f, s, u, PARAMETERS['Km'][0])

    def _resolve_Ko(self):
        if not self._has('Ko'):
            self._assume('Ko', agma.AGMA_DEFAULTS['Ko'], '–')

    def _resolve_Kb(self):
        if not self._has('Kb'):
            self._assume('Kb', agma.AGMA_DEFAULTS['Kb'], '–')

    def _resolve_KT(self):
        if not self._has('KT'):
            self._assume('KT', agma.AGMA_DEFAULTS['KT'], '–')

    def _resolve_KR(self):
        if not self._has('KR'):
            self._assume('KR', agma.AGMA_DEFAULTS['KR'], '–')

    def _resolve_Cp(self):
        if not self._has('Cp'):
            self._assume('Cp', AGMA_SUGGESTIONS['Cp'], '√psi', 'AGMA (steel-steel)')

    def _resolve_Cf(self):
        if not self._has('Cf'):
            self._assume('Cf', agma.AGMA_DEFAULTS['Cf'], '–')

    def _resolve_CH(self):
        if not self._has('CH'):
            self._assume('CH', agma.AGMA_DEFAULTS['CH'], '–')

    def _resolve_J_factor(self):
        if not self._has('J_factor'):
            self._assume('J_factor', AGMA_SUGGESTIONS['J_factor'], '–', 'AGMA Typical (helical)')

    def _resolve_I_factor(self):
        if self._has('I_factor'):
            return
        self._resolve_phi_t()
        self._resolve_psi()
        self._resolve_gear_ratio()
        if self._has('phi_t', 'psi', 'gear_ratio'):
            r, f, s, u = self.c.calc_I_factor(self.known['phi_t'], self.known['psi'], self.known['gear_ratio'])
            self._store('I_factor', r, f, s, u, PARAMETERS['I_factor'][0])

    def _resolve_Nc_p(self):
        if self._has('Nc_p'):
            return
        sf = self.known.get('service_factor', 1.0)
        if self._has('design_life', 'N_pinion'):
            r, f, s, u = self.c.calc_load_cycles(self.known['design_life'], self.known['N_pinion'])
            self._store('Nc_p', r, f, s, u, PARAMETERS['Nc_p'][0])

    def _resolve_YN(self):
        if self._has('YN'):
            return
        self._resolve_Nc_p()
        if self._has('Nc_p'):
            r, f, s, u = self.c.calc_YN(self.known['Nc_p'])
            self._store('YN', r, f, s, u, PARAMETERS['YN'][0])

    def _resolve_ZN(self):
        if self._has('ZN'):
            return
        self._resolve_Nc_p()
        if self._has('Nc_p'):
            r, f, s, u = self.c.calc_ZN(self.known['Nc_p'])
            self._store('ZN', r, f, s, u, PARAMETERS['ZN'][0])

    def _resolve_sat(self):
        if self._has('sat'):
            return
        if self._has('HB'):
            val = agma.calc_sat_from_HB(self.known['HB'])
            self._store('sat', val, "sat = (0.533×HB + 88.3)×1000 psi",
                        f"sat = (0.533×{self.known['HB']} + 88.3)×1000", "psi", PARAMETERS['sat'][0])

    def _resolve_sac(self):
        if self._has('sac'):
            return
        if self._has('HB'):
            val = agma.calc_sac_from_HB(self.known['HB'])
            self._store('sac', val, "sac = 322×HB + 29100 psi",
                        f"sac = 322×{self.known['HB']} + 29100", "psi", PARAMETERS['sac'][0])

    def _resolve_F(self):
        if self._has('F'):
            return
        if self._has('Pn'):
            r, f, s, u = self.c.calc_face_width_from_Pn(self.known['Pn'])
            self._store('F', r, f, s, u, PARAMETERS['F'][0])
            self.assumptions['F'] = (PARAMETERS['F'][0], r, u, 'AGMA: F = 10/Pn')

    def _resolve_SF(self):
        if not self._has('service_factor'):
            self._assume('service_factor', 1.0, '–')

    # ── Main calculation dispatcher ───────────────────────────────
    def calculate(self, input_values: dict, requested_outputs: list):
        """
        input_values: dict of param_id -> float (user-supplied inputs)
        requested_outputs: list of param_id strings

        Returns:
          results: dict of param_id -> float
          calc_details: dict of param_id -> {label, formula, substitution, result, unit}
          assumptions: dict of param_id -> (label, value, unit, source)
          errors: dict of param_id -> error message
        """
        self.reset(input_values)

        # Pre-resolve common dependencies
        self._resolve_psi()
        self._resolve_phi_n()
        self._resolve_Pt()
        self._resolve_Pn()
        self._resolve_phi_t()
        self._resolve_Np()
        self._resolve_Ng()
        self._resolve_gear_ratio()
        self._resolve_Dp()
        self._resolve_Dg()
        self._resolve_F()

        for pid in requested_outputs:
            try:
                self._calculate_one(pid)
            except Exception as e:
                self.errors[pid] = f"Error: {e}"

        return (
            {k: v for k, v in self.known.items() if k in requested_outputs},
            self.calc_details,
            self.assumptions,
            self.errors
        )

    def _calculate_one(self, pid):
        c = self.c
        k = self.known

        # ── GEOMETRY ──────────────────────────────────────────────
        if pid == 'gear_ratio':
            self._resolve_gear_ratio()
            if not self._has('gear_ratio'):
                self.errors[pid] = "Need: Np AND Ng (or Np and N_gear and N_pinion)"

        elif pid == 'Pt':
            self._resolve_Pt()
            if not self._has('Pt'):
                self.errors[pid] = "Need: Pn and ψ"

        elif pid == 'Pn':
            self._resolve_Pn()
            if not self._has('Pn'):
                self.errors[pid] = "Need: Pt and ψ"

        elif pid == 'phi_t':
            self._resolve_phi_t()
            if not self._has('phi_t'):
                self.errors[pid] = "Need: φn and ψ"

        elif pid == 'Dp':
            self._resolve_Dp()
            if not self._has('Dp'):
                self.errors[pid] = "Need: Np and Pt (or Pn and ψ)"

        elif pid == 'Dg':
            self._resolve_Dg()
            if not self._has('Dg'):
                self.errors[pid] = "Need: Ng and Pt (or Pn and ψ)"

        elif pid == 'Np':
            self._resolve_Np()
            if not self._has('Np'):
                self.errors[pid] = "Need: Dp and Pt, or mG and Ng"

        elif pid == 'Ng':
            self._resolve_Ng()
            if not self._has('Ng'):
                self.errors[pid] = "Need: mG and Np, or Dg and Pt"

        elif pid == 'C':
            self._resolve_Dp()
            self._resolve_Dg()
            if self._has('Dp', 'Dg'):
                r, f, s, u = c.calc_center_distance(k['Dp'], k['Dg'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Dp and Dg (or sufficient inputs to compute them)"

        elif pid == 'F':
            self._resolve_F()
            if not self._has('F'):
                self.errors[pid] = "Need: Pn (for AGMA default) or direct input"

        elif pid == 'addendum':
            if not self._has('Pn'):
                self.errors[pid] = "Need: Pn"
            else:
                r, f, s, u = c.calc_addendum(k['Pn'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        elif pid == 'dedendum':
            if not self._has('Pn'):
                self.errors[pid] = "Need: Pn"
            else:
                r, f, s, u = c.calc_dedendum(k['Pn'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        elif pid == 'normal_cp':
            if not self._has('Pn'):
                self.errors[pid] = "Need: Pn"
            else:
                r, f, s, u = c.calc_normal_circular_pitch(k['Pn'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        elif pid == 'trans_cp':
            self._resolve_Pt()
            if not self._has('Pt'):
                self.errors[pid] = "Need: Pt (or Pn and ψ)"
            else:
                r, f, s, u = c.calc_transverse_circular_pitch(k['Pt'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        elif pid == 'base_dia_p':
            self._resolve_Dp()
            self._resolve_phi_t()
            if self._has('Dp', 'phi_t'):
                r, f, s, u = c.calc_base_diameter(k['Dp'], k['phi_t'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Dp and φt"

        elif pid == 'base_dia_g':
            self._resolve_Dg()
            self._resolve_phi_t()
            if self._has('Dg', 'phi_t'):
                r, f, s, u = c.calc_base_diameter(k['Dg'], k['phi_t'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Dg and φt"

        elif pid == 'normal_module':
            if not self._has('Pn'):
                self.errors[pid] = "Need: Pn"
            else:
                r, f, s, u = c.calc_normal_module(k['Pn'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        elif pid == 'trans_module':
            self._resolve_Pt()
            if not self._has('Pt'):
                self.errors[pid] = "Need: Pt"
            else:
                r, f, s, u = c.calc_transverse_module(k['Pt'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])

        # ── POWER & SPEED ─────────────────────────────────────────
        elif pid == 'N_gear':
            self._resolve_gear_ratio()
            if self._has('N_pinion', 'gear_ratio'):
                r, f, s, u = c.calc_RPM_gear(k['N_pinion'], k['gear_ratio'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: N_pinion and mG (or Np and Ng)"

        elif pid == 'HP':
            if self._has('Ft', 'V'):
                r = k['Ft'] * k['V'] / 33000.0
                self._store(pid, r, "HP = Ft × V / 33000",
                            f"HP = {k['Ft']:.2f} × {k['V']:.2f} / 33000", "hp", PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Ft and V"

        # ── FORCE ANALYSIS ────────────────────────────────────────
        elif pid == 'V':
            self._resolve_V()
            if not self._has('V'):
                self.errors[pid] = "Need: Dp and N_pinion"

        elif pid == 'Ft':
            self._resolve_Ft()
            if not self._has('Ft'):
                self.errors[pid] = "Need: HP and V (or Dp and N_pinion)"

        elif pid == 'Fr':
            self._resolve_Ft()
            self._resolve_phi_t()
            if self._has('Ft', 'phi_t'):
                r, f, s, u = c.calc_radial_force(k['Ft'], k['phi_t'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Ft and φt"

        elif pid == 'Fa':
            self._resolve_Ft()
            if self._has('Ft', 'psi'):
                r, f, s, u = c.calc_axial_force(k['Ft'], k['psi'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: Ft and ψ"

        elif pid == 'torque_p':
            if self._has('HP', 'N_pinion'):
                r, f, s, u = c.calc_torque(k['HP'], k['N_pinion'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: HP and N_pinion"

        # ── AGMA FACTORS ──────────────────────────────────────────
        elif pid == 'Kv':
            self._resolve_Kv()
            if not self._has('Kv'):
                self.errors[pid] = "Need: V and Qv"

        elif pid == 'Ks':
            self._resolve_Ks()
            if not self._has('Ks'):
                self.errors[pid] = "Need: Pn, F, and J"

        elif pid == 'Km':
            self._resolve_Km()
            if not self._has('Km'):
                self.errors[pid] = "Need: F and Dp"

        elif pid == 'Ko':
            if not self._has('Ko'):
                self._assume('Ko', agma.AGMA_DEFAULTS['Ko'], '–')

        elif pid == 'Kb':
            if not self._has('Kb'):
                self._assume('Kb', agma.AGMA_DEFAULTS['Kb'], '–')

        elif pid == 'KR':
            if not self._has('KR'):
                self._assume('KR', agma.AGMA_DEFAULTS['KR'], '–')

        elif pid == 'KT':
            if not self._has('KT'):
                self._assume('KT', agma.AGMA_DEFAULTS['KT'], '–')

        elif pid == 'Cp':
            self._resolve_Cp()

        elif pid == 'J_factor':
            self._resolve_J_factor()

        elif pid == 'I_factor':
            self._resolve_I_factor()
            if not self._has('I_factor'):
                self.errors[pid] = "Need: φt, ψ, and mG"

        elif pid == 'Qv':
            if not self._has('Qv'):
                self._assume('Qv', agma.AGMA_DEFAULTS['Qv'], '–')

        elif pid == 'Cf':
            self._resolve_Cf()

        elif pid == 'CH':
            self._resolve_CH()

        elif pid == 'YN':
            self._resolve_YN()
            if not self._has('YN'):
                self.errors[pid] = "Need: Nc_p (or design_life and N_pinion)"

        elif pid == 'ZN':
            self._resolve_ZN()
            if not self._has('ZN'):
                self.errors[pid] = "Need: Nc_p (or design_life and N_pinion)"

        # ── STRESS ANALYSIS ───────────────────────────────────────
        elif pid == 'sigma_b':
            self._resolve_Ft()
            self._resolve_Ko()
            self._resolve_Kv()
            self._resolve_Ks()
            self._resolve_Km()
            self._resolve_Kb()
            self._resolve_J_factor()
            if self._has('Ft', 'Pn', 'F', 'J_factor', 'Ko', 'Kv', 'Ks', 'Km', 'Kb'):
                r, f, s, u = c.calc_bending_stress(
                    k['Ft'], k['Pn'], k['F'], k['J_factor'],
                    k['Ko'], k['Kv'], k['Ks'], k['Km'], k['Kb'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                missing = [p for p in ['Ft', 'Pn', 'F', 'J_factor', 'Ko', 'Kv', 'Ks', 'Km', 'Kb']
                           if not self._has(p)]
                self.errors[pid] = f"Need: {', '.join(missing)}"

        elif pid == 'sigma_c':
            self._resolve_Ft()
            self._resolve_Ko()
            self._resolve_Kv()
            self._resolve_Ks()
            self._resolve_Km()
            self._resolve_Cp()
            self._resolve_Cf()
            self._resolve_I_factor()
            self._resolve_Dp()
            if self._has('Cp', 'Ft', 'Ko', 'Kv', 'Ks', 'Dp', 'F', 'I_factor', 'Km', 'Cf'):
                r, f, s, u = c.calc_contact_stress(
                    k['Cp'], k['Ft'], k['Ko'], k['Kv'], k['Ks'],
                    k['Dp'], k['F'], k['I_factor'], k['Km'], k['Cf'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                missing = [p for p in ['Cp', 'Ft', 'Ko', 'Kv', 'Ks', 'Dp', 'F', 'I_factor', 'Km', 'Cf']
                           if not self._has(p)]
                self.errors[pid] = f"Need: {', '.join(missing)}"

        elif pid == 'sigma_b_allow':
            self._resolve_sat()
            self._resolve_YN()
            self._resolve_KT()
            self._resolve_KR()
            self._resolve_SF()
            if self._has('sat', 'YN', 'KT', 'KR', 'service_factor'):
                r, f, s, u = c.calc_allowable_bending_stress(
                    k['sat'], k['YN'], k['KT'], k['KR'], k['service_factor'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                missing = [p for p in ['sat', 'YN', 'KT', 'KR'] if not self._has(p)]
                self.errors[pid] = f"Need: {', '.join(missing)}"

        elif pid == 'sigma_c_allow':
            self._resolve_sac()
            self._resolve_ZN()
            self._resolve_CH()
            self._resolve_KT()
            self._resolve_KR()
            self._resolve_SF()
            if self._has('sac', 'ZN', 'CH', 'KT', 'KR', 'service_factor'):
                r, f, s, u = c.calc_allowable_contact_stress(
                    k['sac'], k['ZN'], k['CH'], k['KT'], k['KR'], k['service_factor'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                missing = [p for p in ['sac', 'ZN', 'CH', 'KT', 'KR'] if not self._has(p)]
                self.errors[pid] = f"Need: {', '.join(missing)}"

        elif pid == 'SF_b':
            # Need both sigma_b and sigma_b_allow
            self._calculate_one('sigma_b')
            self._calculate_one('sigma_b_allow')
            if self._has('sigma_b_allow', 'sigma_b'):
                r, f, s, u = c.calc_bending_safety_factor(k['sigma_b_allow'], k['sigma_b'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: σat and σt (compute bending stress and allowable first)"

        elif pid == 'SF_c':
            self._calculate_one('sigma_c')
            self._calculate_one('sigma_c_allow')
            if self._has('sigma_c_allow', 'sigma_c'):
                r, f, s, u = c.calc_contact_safety_factor(k['sigma_c_allow'], k['sigma_c'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: σac and σc (compute contact stress and allowable first)"

        # ── MATERIAL ──────────────────────────────────────────────
        elif pid == 'sat':
            self._resolve_sat()
            if not self._has('sat'):
                self.errors[pid] = "Need: HB (Brinell hardness)"

        elif pid == 'sac':
            self._resolve_sac()
            if not self._has('sac'):
                self.errors[pid] = "Need: HB (Brinell hardness)"

        elif pid in ('HB', 'su', 'sy'):
            if not self._has(pid):
                self.errors[pid] = f"'{PARAMETERS[pid][0]}' must be provided as input."

        # ── DESIGN ────────────────────────────────────────────────
        elif pid == 'Nc_p':
            self._resolve_Nc_p()
            if not self._has('Nc_p'):
                self.errors[pid] = "Need: design_life (hours) and N_pinion (rpm)"

        elif pid == 'efficiency':
            if self._has('psi', 'phi_n'):
                r, f, s, u = c.calc_efficiency(k['psi'], k['phi_n'])
                self._store(pid, r, f, s, u, PARAMETERS[pid][0])
            else:
                self.errors[pid] = "Need: ψ and φn"

        elif pid == 'service_factor':
            self._resolve_SF()

        elif pid == 'design_life':
            if not self._has('design_life'):
                self.errors[pid] = "Design life must be provided as input."

    def get_design_status(self):
        """Return design verification status dict"""
        status = {'status': 'INCOMPLETE - No stress analysis', 'notes': []}
        k = self.known

        if 'SF_b' in k and 'SF_c' in k:
            sfb = k['SF_b']
            sfc = k['SF_c']
            if sfb >= 1.2 and sfc >= 1.2:
                status['status'] = 'PASS - Design is adequate'
            elif sfb < 1.0 or sfc < 1.0:
                status['status'] = 'FAIL - Design is inadequate'
            else:
                status['status'] = 'MARGINAL - Safety factors below 1.2'
            status['notes'].append(f"Bending Safety Factor SFb = {sfb:.3f} {'✓' if sfb >= 1.2 else '✗'}")
            status['notes'].append(f"Contact Safety Factor SFc = {sfc:.3f} {'✓' if sfc >= 1.2 else '✗'}")
        elif 'SF_b' in k:
            sfb = k['SF_b']
            status['status'] = 'PARTIAL - Bending check only'
            status['notes'].append(f"Bending Safety Factor SFb = {sfb:.3f} {'✓' if sfb >= 1.2 else '✗'}")
        elif 'SF_c' in k:
            sfc = k['SF_c']
            status['status'] = 'PARTIAL - Contact check only'
            status['notes'].append(f"Contact Safety Factor SFc = {sfc:.3f} {'✓' if sfc >= 1.2 else '✗'}")

        if 'sigma_b' in k:
            status['notes'].append(f"Bending Stress σt = {k['sigma_b']:.1f} psi")
        if 'sigma_c' in k:
            status['notes'].append(f"Contact Stress σc = {k['sigma_c']:.1f} psi")
        if 'V' in k:
            v = k['V']
            if v > 3600:
                status['notes'].append(f"WARNING: Pitch line velocity V = {v:.0f} ft/min (high, consider higher Qv)")

        return status


# ─────────────────────────────────────────────────────────────────────────────
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Helical Gear Design Software  |  AGMA Standards  |  Imperial Units")
        self.resize(1400, 900)

        self.dark_mode = True
        self.param_rows: dict[str, ParameterRow] = {}
        self.engine = CalculationEngine()
        self.report_gen = ReportGenerator()
        self._last_calc_details = {}
        self._last_assumptions = {}
        self._last_inputs = {}

        self._build_ui()
        self._apply_style()

    # ── UI Construction ───────────────────────────────────────────
    def _build_ui(self):
        # Central widget + main layout
        central = QWidget()
        self.setCentralWidget(central)
        main_vbox = QVBoxLayout(central)
        main_vbox.setContentsMargins(8, 8, 8, 8)
        main_vbox.setSpacing(6)

        # ── Header bar ───────────────────────────────────────────
        header = self._build_header()
        main_vbox.addWidget(header)

        # ── Splitter: left (params) | right (results) ────────────
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(6)

        left_panel = self._build_left_panel()
        right_panel = self._build_right_panel()

        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([620, 780])
        main_vbox.addWidget(splitter, 1)

        # ── Bottom bar ───────────────────────────────────────────
        bottom = self._build_bottom_bar()
        main_vbox.addWidget(bottom)

        # Status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready  |  AGMA Helical Gear Design Software  |  Imperial Units")

    def _build_header(self):
        frame = QFrame()
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(12, 8, 12, 8)

        title = QLabel("Helical Gear Design Software")
        title.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        layout.addWidget(title)

        subtitle = QLabel("AGMA 2001 Standards  |  Imperial (Inch) System")
        layout.addWidget(subtitle)
        layout.addStretch()

        # Toolbar buttons
        self.btn_save = QPushButton("Save Session")
        self.btn_load = QPushButton("Load Session")
        self.btn_theme = QPushButton("Light Mode")
        self.btn_theme.setCheckable(True)
        self.btn_clear_all = QPushButton("Clear All")
        self.btn_clear_all.setObjectName("btn_clear")

        for btn in (self.btn_save, self.btn_load, self.btn_theme, self.btn_clear_all):
            btn.setMinimumWidth(90)
            layout.addWidget(btn)

        self.btn_save.clicked.connect(self._save_session)
        self.btn_load.clicked.connect(self._load_session)
        self.btn_theme.clicked.connect(self._toggle_theme)
        self.btn_clear_all.clicked.connect(self._clear_all)

        return frame

    def _build_left_panel(self):
        widget = QWidget()
        vbox = QVBoxLayout(widget)
        vbox.setContentsMargins(0, 0, 0, 0)
        vbox.setSpacing(4)

        # Top controls
        ctrl = QHBoxLayout()
        lbl_info = QLabel("Select Input/Output role for each parameter, enter input values, then Calculate.")
        lbl_info.setWordWrap(True)
        ctrl.addWidget(lbl_info, 1)

        agma_all_btn = QPushButton("Apply AGMA Defaults to All Inputs")
        agma_all_btn.setObjectName("btn_agma")
        agma_all_btn.clicked.connect(self._apply_all_agma_defaults)
        ctrl.addWidget(agma_all_btn)
        vbox.addLayout(ctrl)

        # Scroll area for parameter rows
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        container = QWidget()
        self.params_layout = QVBoxLayout(container)
        self.params_layout.setContentsMargins(4, 4, 4, 4)
        self.params_layout.setSpacing(2)

        # Build rows by category
        for cat in CATEGORIES:
            group = QGroupBox(cat)
            g_layout = QVBoxLayout(group)
            g_layout.setSpacing(2)
            g_layout.setContentsMargins(6, 14, 6, 6)

            for pid, (label, unit, category) in PARAMETERS.items():
                if category == cat:
                    row = ParameterRow(pid, label, unit)
                    row.mode_changed.connect(self._on_param_mode_changed)
                    self.param_rows[pid] = row
                    g_layout.addWidget(row)

            self.params_layout.addWidget(group)

        self.params_layout.addStretch()
        scroll.setWidget(container)
        vbox.addWidget(scroll, 1)

        return widget

    def _build_right_panel(self):
        widget = QWidget()
        vbox = QVBoxLayout(widget)
        vbox.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()

        # Tab 1: Results
        results_tab = QWidget()
        r_vbox = QVBoxLayout(results_tab)
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        self.results_text.setFont(QFont("Courier New", 11))
        r_vbox.addWidget(self.results_text)
        self.tab_widget.addTab(results_tab, "Calculation Results")

        # Tab 2: Assumed Values
        assume_tab = QWidget()
        a_vbox = QVBoxLayout(assume_tab)
        self.assume_text = QTextEdit()
        self.assume_text.setReadOnly(True)
        self.assume_text.setFont(QFont("Courier New", 11))
        a_vbox.addWidget(self.assume_text)
        self.tab_widget.addTab(assume_tab, "Assumed Values")

        # Tab 3: Full Report
        report_tab = QWidget()
        rp_vbox = QVBoxLayout(report_tab)
        self.report_text = QTextEdit()
        self.report_text.setReadOnly(True)
        self.report_text.setFont(QFont("Courier New", 10))
        btn_row = QHBoxLayout()
        self.btn_export_pdf = QPushButton("Export PDF")
        self.btn_export_pdf.setObjectName("btn_export_pdf")
        self.btn_export_excel = QPushButton("Export Excel")
        self.btn_export_excel.setObjectName("btn_export_excel")
        self.btn_export_pdf.clicked.connect(self._export_pdf)
        self.btn_export_excel.clicked.connect(self._export_excel)
        btn_row.addWidget(self.btn_export_pdf)
        btn_row.addWidget(self.btn_export_excel)
        btn_row.addStretch()
        rp_vbox.addLayout(btn_row)
        rp_vbox.addWidget(self.report_text)
        self.tab_widget.addTab(report_tab, "Full Report")

        # Tab 4: AGMA Reference
        ref_tab = QWidget()
        rv_vbox = QVBoxLayout(ref_tab)
        ref_text = QTextEdit()
        ref_text.setReadOnly(True)
        ref_text.setFont(QFont("Courier New", 10))
        ref_text.setText(self._build_reference_text())
        rv_vbox.addWidget(ref_text)
        self.tab_widget.addTab(ref_tab, "AGMA Reference")

        vbox.addWidget(self.tab_widget)
        return widget

    def _build_bottom_bar(self):
        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setContentsMargins(4, 4, 4, 4)

        self.btn_calculate = QPushButton("CALCULATE")
        self.btn_calculate.setObjectName("btn_calculate")
        self.btn_calculate.setMinimumWidth(180)
        self.btn_calculate.clicked.connect(self._run_calculation)
        layout.addWidget(self.btn_calculate)

        self.calc_status_label = QLabel("Select inputs/outputs and click Calculate.")
        layout.addWidget(self.calc_status_label, 1)

        return frame

    # ── Style ─────────────────────────────────────────────────────
    def _apply_style(self):
        if self.dark_mode:
            self.setStyleSheet(DARK_STYLE)
            self.btn_theme.setText("Light Mode")
        else:
            self.setStyleSheet(LIGHT_STYLE)
            self.btn_theme.setText("Dark Mode")

    def _toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self._apply_style()

    # ── Slots ─────────────────────────────────────────────────────
    def _on_param_mode_changed(self, pid, mode):
        row = self.param_rows[pid]
        if mode == 'output':
            row.clear_result()

    def _apply_all_agma_defaults(self):
        for pid, row in self.param_rows.items():
            if row.get_mode() == 'input' and pid in AGMA_SUGGESTIONS:
                if not row.get_value():
                    row.set_value(AGMA_SUGGESTIONS[pid])

    # ── Main Calculation ──────────────────────────────────────────
    def _run_calculation(self):
        # Gather inputs
        input_values = {}
        requested_outputs = []
        input_labels = {}

        for pid, row in self.param_rows.items():
            mode = row.get_mode()
            if mode == 'input':
                val = row.get_value()
                if val is not None:
                    input_values[pid] = val
                    input_labels[pid] = (PARAMETERS[pid][0], val, PARAMETERS[pid][1])
                else:
                    # Missing input
                    row.set_result("⚠ No value entered", error=True)
            elif mode == 'output':
                requested_outputs.append(pid)

        if not requested_outputs:
            QMessageBox.information(self, "No Outputs Selected",
                                    "Please select at least one parameter as Output.")
            return

        # Run engine
        results, calc_details, assumptions, errors = self.engine.calculate(
            input_values, requested_outputs)

        self._last_calc_details = calc_details
        self._last_assumptions = assumptions
        self._last_inputs = input_labels

        # Update row results
        for pid in requested_outputs:
            row = self.param_rows[pid]
            if pid in errors:
                row.set_result(f"Missing: {errors[pid]}", error=True)
            elif pid in calc_details:
                d = calc_details[pid]
                row.set_result(d['result'], d['unit'])
            elif pid in assumptions:
                a = assumptions[pid]
                row.set_result(a[1], a[2], warning=True)
            else:
                row.set_result("Not computed", error=True)

        # Build results display
        self._show_results(calc_details, assumptions, errors)
        self._show_assumptions(assumptions)
        self._show_report(input_labels, calc_details, assumptions, errors)

        # Update status
        n_ok = len(calc_details)
        n_err = len(errors)
        status_msg = f"Calculated {n_ok} outputs"
        if n_err:
            status_msg += f"  |  {n_err} errors (missing inputs)"
        self.calc_status_label.setText(status_msg)
        self.status_bar.showMessage(status_msg)
        self.tab_widget.setCurrentIndex(0)

    def _show_results(self, calc_details, assumptions, errors):
        lines = []
        lines.append("=" * 65)
        lines.append("  CALCULATION RESULTS")
        lines.append("=" * 65)

        if calc_details:
            lines.append("\nCOMPUTED OUTPUTS:")
            lines.append("─" * 65)
            for pid, d in calc_details.items():
                lines.append(f"\n  [{d['label']}]")
                lines.append(f"  Formula      : {d['formula']}")
                for line in d['substitution'].split('\n'):
                    lines.append(f"  Substitution : {line}")
                if isinstance(d['result'], float):
                    lines.append(f"  Result       : {d['result']:.6g} {d['unit']}")
                else:
                    lines.append(f"  Result       : {d['result']} {d['unit']}")

        if errors:
            lines.append("\n\nERRORS (missing inputs):")
            lines.append("─" * 65)
            for pid, msg in errors.items():
                lines.append(f"  {PARAMETERS[pid][0]}: {msg}")

        self.results_text.setText("\n".join(lines))

    def _show_assumptions(self, assumptions):
        lines = []
        lines.append("=" * 65)
        lines.append("  ASSUMED VALUES  (AGMA Standard or Default)")
        lines.append("=" * 65)
        lines.append("")

        if not assumptions:
            lines.append("  No assumptions were made.")
            lines.append("  All required values were provided as inputs.")
        else:
            lines.append(f"  {'Parameter':<44} {'Value':>10}  {'Unit':<12}  Source")
            lines.append("  " + "─" * 62)
            for pid, (label, val, unit, source) in assumptions.items():
                if isinstance(val, float):
                    val_str = f"{val:.4g}"
                else:
                    val_str = str(val)
                lines.append(f"  {label:<44} {val_str:>10}  {unit:<12}  {source}")

        lines.append("")
        lines.append("=" * 65)
        lines.append("NOTE: Assumed values are based on AGMA 2001 standard recommendations.")
        lines.append("Review and override these values as appropriate for your application.")

        self.assume_text.setText("\n".join(lines))

    def _show_report(self, inputs, calc_details, assumptions, errors):
        design_status = self.engine.get_design_status()
        report = self.report_gen.generate_text_report(
            inputs, {}, assumptions, calc_details, design_status)
        self.report_text.setText(report)

    # ── Clear / Save / Load ───────────────────────────────────────
    def _clear_all(self):
        reply = QMessageBox.question(self, "Clear All",
                                     "Reset all parameters to default state?",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            for row in self.param_rows.values():
                row.reset()
            self.results_text.clear()
            self.assume_text.clear()
            self.report_text.clear()
            self.calc_status_label.setText("All parameters cleared.")
            self.status_bar.showMessage("Session cleared.")

    def _save_session(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save Session", "", "JSON Files (*.json)")
        if not path:
            return
        session = {}
        for pid, row in self.param_rows.items():
            session[pid] = {
                'mode': row.get_mode(),
                'value': row.value_edit.text(),
            }
        try:
            with open(path, 'w') as f:
                json.dump(session, f, indent=2)
            self.status_bar.showMessage(f"Session saved to {path}")
        except Exception as e:
            QMessageBox.critical(self, "Save Error", str(e))

    def _load_session(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Load Session", "", "JSON Files (*.json)")
        if not path:
            return
        try:
            with open(path) as f:
                session = json.load(f)
            for pid, data in session.items():
                if pid in self.param_rows:
                    row = self.param_rows[pid]
                    mode = data.get('mode', 'none')
                    if mode == 'input':
                        row.rb_input.setChecked(True)
                    elif mode == 'output':
                        row.rb_output.setChecked(True)
                    else:
                        row.rb_none.setChecked(True)
                    row.value_edit.setText(data.get('value', ''))
            self.status_bar.showMessage(f"Session loaded from {path}")
        except Exception as e:
            QMessageBox.critical(self, "Load Error", str(e))

    # ── Export ────────────────────────────────────────────────────
    def _export_pdf(self):
        if not self._last_calc_details:
            QMessageBox.information(self, "No Results", "Run calculation first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export PDF", "gear_design_report.pdf", "PDF Files (*.pdf);;HTML Files (*.html)")
        if not path:
            return
        report_text = self.report_text.toPlainText()
        ok, msg = self.report_gen.export_pdf(report_text, path)
        if ok:
            QMessageBox.information(self, "Export Complete", f"PDF saved to:\n{path}")
        else:
            QMessageBox.warning(self, "Export Notice", msg)

    def _export_excel(self):
        if not self._last_calc_details:
            QMessageBox.information(self, "No Results", "Run calculation first.")
            return
        path, _ = QFileDialog.getSaveFileName(
            self, "Export Excel", "gear_design_report.xlsx",
            "Excel Files (*.xlsx);;CSV Files (*.csv)")
        if not path:
            return
        ok, msg = self.report_gen.export_excel(
            self._last_inputs, {}, self._last_assumptions, self._last_calc_details, path)
        if ok:
            QMessageBox.information(self, "Export Complete", f"Excel saved to:\n{path}")
        else:
            QMessageBox.warning(self, "Export Notice", msg)

    # ── Reference Text ────────────────────────────────────────────
    def _build_reference_text(self):
        lines = []
        lines.append("=" * 65)
        lines.append("  AGMA REFERENCE DATA")
        lines.append("=" * 65)
        lines.append("")
        lines.append("STANDARD NORMAL DIAMETRAL PITCHES (Pn, in⁻¹):")
        lines.append("  " + "  ".join(str(p) for p in agma.STANDARD_DIAMETRAL_PITCHES))
        lines.append("")
        lines.append("STANDARD HELIX ANGLES (ψ, degrees):")
        lines.append("  " + "  ".join(str(p) for p in agma.STANDARD_HELIX_ANGLES))
        lines.append("")
        lines.append("STANDARD NORMAL PRESSURE ANGLES (φn, degrees):")
        lines.append("  " + "  ".join(str(p) for p in agma.STANDARD_PRESSURE_ANGLES))
        lines.append("")
        lines.append("QUALITY NUMBERS (Qv):")
        for qv, desc in agma.QUALITY_NUMBERS.items():
            lines.append(f"  Qv = {qv:2d}  {desc}")
        lines.append("")
        lines.append("ELASTIC COEFFICIENT Cp (√psi):")
        for (m1, m2), cp in agma.ELASTIC_COEFFICIENT.items():
            lines.append(f"  {m1:<12} / {m2:<12}: Cp = {cp}")
        lines.append("")
        lines.append("RELIABILITY FACTOR KR:")
        for r, kr in sorted(agma.Kr_TABLE.items()):
            lines.append(f"  Reliability {r*100:.1f}%: KR = {kr}")
        lines.append("")
        lines.append("OVERLOAD FACTOR Ko (Table 9-5):")
        lines.append("  Source \\ Driven  Uniform  Light Shock  Mod. Shock  Heavy Shock")
        lines.append("  Uniform           1.00       1.25         1.50")
        lines.append("  Light Shock       1.10       1.35         1.60")
        lines.append("  Moderate Shock    1.25       1.50         1.75")
        lines.append("  Heavy Shock       1.50       1.75                   2.00")
        lines.append("")
        lines.append("MATERIAL ALLOWABLE STRESSES:")
        lines.append(f"  {'Material':<40} {'sat (psi)':>10}  {'sac (psi)':>10}  HB")
        lines.append("  " + "─" * 62)
        for key, mat in agma.MATERIAL_DATA.items():
            lines.append(f"  {mat['description']:<40} {mat['sat']:>10}  {mat['sac']:>10}  {mat['HB']}")
        lines.append("")
        lines.append("DESIGN LIFE RECOMMENDATIONS (hours):")
        for app, (lo, hi) in agma.DESIGN_LIFE.items():
            lines.append(f"  {app.replace('_', ' ').title():<40}: {lo:,} – {hi:,} hr")
        lines.append("")
        lines.append("FACE WIDTH GUIDELINE (AGMA):")
        lines.append("  10/Pn ≤ F ≤ 12/Pn  (face width in inches)")
        lines.append("")
        lines.append("KEY FORMULAS SUMMARY:")
        lines.append("  Pt = Pn × cos(ψ)")
        lines.append("  φt = arctan(tan(φn) / cos(ψ))")
        lines.append("  Dp = Np / Pt,  Dg = Ng / Pt")
        lines.append("  C  = (Dp + Dg) / 2")
        lines.append("  V  = π × Dp × N / 12  [ft/min]")
        lines.append("  Ft = 33,000 × HP / V")
        lines.append("  σt = (Ft×Pn / (F×J)) × Ko×Kv×Ks×Km×Kb  [AGMA bending]")
        lines.append("  σc = Cp × √(Ft×Ko×Kv×Ks×Km×Cf / (Dp×F×I))  [AGMA contact]")
        lines.append("  Kv = ((A + √V) / A)^B  where B=0.25×(12-Qv)^(2/3)")
        lines.append("  Nc = 60 × L × n × q  [load cycles]")

        return "\n".join(lines)
