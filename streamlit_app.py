"""
Helical Gear Calculator — Streamlit Application
PD-Based Method · Inch Units · Engineering Grade
"""

import io
import math

import streamlit as st
import plotly.graph_objects as go

from calculations.gear_calculator import validate_inputs, calculate_gears

# ─────────────────────────────────────────────
# Page config (must be first Streamlit call)
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Helical Gear Calculator",
    page_icon="⚙",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
# Custom CSS — dark engineering theme
# ─────────────────────────────────────────────
st.markdown("""
<style>
/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'Inter', 'Segoe UI', system-ui, sans-serif;
}
.stApp {
    background: #0d1b2a;
    color: #e8edf2;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #1a2535 !important;
    border-right: 1px solid rgba(30,144,255,0.18);
}
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3 {
    color: #4dabff;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    border-bottom: 1px solid rgba(30,144,255,0.18);
    padding-bottom: 6px;
    margin-top: 1.2rem;
}

/* ── Number inputs ── */
[data-testid="stNumberInput"] input {
    background: #1e2d3d !important;
    border: 1.5px solid rgba(30,144,255,0.25) !important;
    border-radius: 8px !important;
    color: #e8edf2 !important;
    font-family: 'JetBrains Mono', 'Fira Code', monospace !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: #1e90ff !important;
    box-shadow: 0 0 0 3px rgba(30,144,255,0.15) !important;
}

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: rgba(30,45,61,0.75);
    border: 1px solid rgba(30,144,255,0.18);
    border-radius: 12px;
    padding: 14px 18px !important;
    border-top: 3px solid #1e90ff;
}
[data-testid="stMetricLabel"] { color: #8ca0b5 !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: 0.05em; }
[data-testid="stMetricValue"] { color: #4dabff !important; font-family: 'JetBrains Mono', monospace !important; font-size: 1.4rem !important; font-weight: 800 !important; }
[data-testid="stMetricDelta"] { font-size: 0.72rem !important; }

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #1e90ff, #0f5fa8);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    font-size: 0.88rem;
    padding: 10px 24px;
    transition: all 0.2s;
    box-shadow: 0 2px 12px rgba(30,144,255,0.35);
    width: 100%;
}
.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(30,144,255,0.5);
}

/* ── Download buttons ── */
[data-testid="stDownloadButton"] > button {
    background: linear-gradient(135deg, #1e90ff, #0f5fa8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    width: 100%;
}

/* ── Checkboxes ── */
[data-testid="stCheckbox"] label {
    color: #8ca0b5;
    font-size: 0.83rem;
    font-weight: 500;
}
[data-testid="stCheckbox"] label:hover { color: #e8edf2; }

/* ── Dataframe / Table ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }
.stDataFrame thead th { background: #0d1b2a !important; color: #4dabff !important; }

/* ── Info / Warning / Error boxes ── */
[data-testid="stAlert"] {
    border-radius: 8px;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #1e2d3d !important;
    border-radius: 8px !important;
    color: #4dabff !important;
    font-weight: 600 !important;
}

/* ── Divider ── */
hr { border-color: rgba(30,144,255,0.15) !important; }

/* ── Header banner ── */
.header-banner {
    background: linear-gradient(135deg, #0d1b2a 0%, #112233 100%);
    border: 1px solid rgba(30,144,255,0.2);
    border-radius: 14px;
    padding: 22px 28px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 18px;
}
.header-icon {
    font-size: 48px;
    line-height: 1;
}
.header-title { margin: 0; font-size: 1.7rem; font-weight: 800; color: #e8edf2; }
.header-sub   { margin: 4px 0 0; font-size: 0.82rem; color: #4dabff; letter-spacing: 0.06em; text-transform: uppercase; }

/* ── Result card ── */
.res-card {
    background: rgba(30,45,61,0.75);
    border: 1px solid rgba(30,144,255,0.18);
    border-top: 3px solid #1e90ff;
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.res-card .rc-label { font-size: 0.72rem; color: #8ca0b5; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; margin-bottom: 4px; }
.res-card .rc-value { font-size: 1.55rem; font-weight: 800; color: #4dabff; font-family: monospace; line-height: 1; }
.res-card .rc-unit  { font-size: 0.72rem; color: #8ca0b5; margin-top: 2px; }
.res-card .rc-formula { font-size: 0.7rem; color: rgba(30,144,255,0.65); font-family: monospace; margin-top: 8px; }

/* ── Formula card ── */
.formula-card {
    background: #1e2d3d;
    border: 1px solid rgba(30,144,255,0.15);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 10px;
}
.formula-card .fc-name { font-size: 0.72rem; color: #8ca0b5; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; margin-bottom: 4px; }
.formula-card .fc-eq   { font-family: monospace; font-size: 0.85rem; color: #00d4aa; margin-bottom: 4px; }
.formula-card .fc-desc { font-size: 0.75rem; color: #8ca0b5; line-height: 1.5; }

/* ── Warning card ── */
.warn-card {
    background: rgba(255,183,77,0.08);
    border: 1px solid rgba(255,183,77,0.35);
    border-radius: 10px;
    padding: 12px 16px;
    margin-bottom: 12px;
    color: #ffb74d;
    font-size: 0.83rem;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Header banner
# ─────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <div class="header-icon">⚙</div>
  <div>
    <div class="header-title">Helical Gear Calculator</div>
    <div class="header-sub">PD-Based Method &nbsp;·&nbsp; Inch Units &nbsp;·&nbsp; Engineering Grade</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# SIDEBAR — Inputs
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙ Input Parameters")

    # ── Gear Geometry ──
    st.markdown("### 📐 Gear Geometry")
    PD   = st.number_input("Pitch Diameter — PD (in)",    min_value=0.1,   max_value=200.0,    value=4.0,   step=0.1,   help="Primary design parameter. Diameter of the pitch circle in inches.")
    Z    = st.number_input("Number of Teeth — Z",         min_value=6,     max_value=500,      value=20,    step=1,     help="Total tooth count. Must be a whole number. Defines gear size with PD.")
    beta = st.number_input("Helix Angle — β (°)",         min_value=1.0,   max_value=89.0,     value=20.0,  step=0.5,   help="Angle between tooth helix and gear axis. Typical: 15°–35°.")
    phi  = st.number_input("Normal Pressure Angle — φ (°)", min_value=1.0, max_value=45.0,     value=20.0,  step=0.5,   help="Standard values: 14.5°, 20°, 25°. Determines tooth profile shape.")
    F    = st.number_input("Face Width — F (in)",         min_value=0.01,  max_value=100.0,    value=2.0,   step=0.1,   help="Tooth length along gear axis. Typical: 0.5×PD to 2×PD.")

    # ── Operating Conditions ──
    st.markdown("### ⚡ Operating Conditions")
    HP   = st.number_input("Input Power — HP",            min_value=0.001, max_value=100000.0, value=10.0,  step=0.5,   help="Transmitted power in horsepower. Used to calculate torque and forces.")
    RPM  = st.number_input("Rotational Speed (RPM)",      min_value=1.0,   max_value=100000.0, value=1750.0,step=50.0,  help="Shaft speed. T = HP × 63,025 / RPM (lb·in).")

    # ── Gear Pair ──
    st.markdown("### ⚙ Gear Pair Information")
    Z1   = st.number_input("Pinion Teeth — Z₁",          min_value=6,     max_value=500,      value=18,    step=1,     help="Teeth on the driving pinion (smaller gear).")
    Z2   = st.number_input("Gear Teeth — Z₂",            min_value=6,     max_value=500,      value=54,    step=1,     help="Teeth on the driven gear. Gear Ratio = Z₂ / Z₁.")

    # ── Load Factors ──
    st.markdown("### 🔧 Load Factors")
    Ks   = st.number_input("Service Factor — Ks",        min_value=0.5,   max_value=5.0,      value=1.25,  step=0.05,  help="Shock/dynamic load multiplier. 1.0=uniform, 1.25=moderate, 1.5–2.0=heavy shock.")

    st.markdown("---")

    # ── Output Selection ──
    st.markdown("### ✅ Output Selection")
    st.caption("Choose which parameters to calculate:")

    col_a, col_b = st.columns(2)
    select_all   = col_a.button("Select All")
    clear_all    = col_b.button("Clear All")

    # Track selection state
    if "sel" not in st.session_state:
        st.session_state.sel = {
            "diametral_pitch": True,
            "circular_pitch": True,
            "base_circle_diameter": True,
            "outside_diameter": True,
            "root_diameter": True,
            "lead": True,
            "gear_ratio": True,
            "tangential_force": True,
            "axial_force": True,
            "torque": True,
        }

    if select_all:
        for k in st.session_state.sel:
            st.session_state.sel[k] = True
    if clear_all:
        for k in st.session_state.sel:
            st.session_state.sel[k] = False

    OUTPUT_LABELS = {
        "diametral_pitch":      "⚙ Diametral Pitch",
        "circular_pitch":       "⭕ Circular Pitch",
        "base_circle_diameter": "🔵 Base Circle Dia.",
        "outside_diameter":     "📐 Outside Diameter",
        "root_diameter":        "📏 Root Diameter",
        "lead":                 "↕ Lead",
        "gear_ratio":           "⚖ Gear Ratio",
        "tangential_force":     "➡ Tangential Force",
        "axial_force":          "⬆ Axial Force",
        "torque":               "🔄 Torque",
    }

    for key, label in OUTPUT_LABELS.items():
        st.session_state.sel[key] = st.checkbox(
            label, value=st.session_state.sel[key], key=f"cb_{key}"
        )

    st.markdown("---")
    calc_btn = st.button("⚡ Calculate", use_container_width=True)

# ─────────────────────────────────────────────
# Build raw input dict
# ─────────────────────────────────────────────
raw_inputs = {
    "pitch_diameter": str(PD),
    "num_teeth":      str(int(Z)),
    "helix_angle":    str(beta),
    "pressure_angle": str(phi),
    "face_width":     str(F),
    "power":          str(HP),
    "rpm":            str(RPM),
    "pinion_teeth":   str(int(Z1)),
    "gear_teeth":     str(int(Z2)),
    "service_factor": str(Ks),
}

selected_outputs = [k for k, v in st.session_state.sel.items() if v]

# ─────────────────────────────────────────────
# Run calculation on button press
# ─────────────────────────────────────────────
if calc_btn:
    if not selected_outputs:
        st.error("⛔ Please select at least one output parameter.")
        st.stop()

    parsed, errors = validate_inputs(raw_inputs)

    if errors:
        st.error("**Input Errors:**\n" + "\n".join(f"- {e}" for e in errors))
        st.stop()

    calc = calculate_gears(parsed, selected_outputs)
    results  = calc["results"]
    warnings = calc["warnings"]

    # Store in session so exports work without re-click
    st.session_state["last_calc"]   = calc
    st.session_state["last_parsed"] = parsed

    # ── Warnings ──
    for w in warnings:
        st.markdown(f'<div class="warn-card">⚠ {w}</div>', unsafe_allow_html=True)

    # ── Metric cards (4 per row) ──
    st.markdown("### 📊 Results")
    keys = list(results.keys())
    for row_start in range(0, len(keys), 4):
        cols = st.columns(4)
        for col, key in zip(cols, keys[row_start:row_start + 4]):
            r = results[key]
            col.metric(
                label=r["label"],
                value=f"{r['value']}",
                delta=r["unit"],
            )

    st.markdown("---")

    # ── Summary table ──
    with st.expander("📋 Engineering Summary Table", expanded=True):
        import pandas as pd
        rows = []
        for key, r in results.items():
            rows.append({
                "Parameter":   r["label"],
                "Value":       r["value"],
                "Unit":        r["unit"],
                "Formula":     r["formula"],
                "Description": r["description"],
            })
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

    # ── Chart ──
    chart_keys = ["tangential_force", "axial_force", "torque"]
    chart_data = {k: results[k] for k in chart_keys if k in results}
    if chart_data:
        with st.expander("📈 Force & Torque Chart", expanded=True):
            labels = [v["label"] for v in chart_data.values()]
            values = [float(v["value"]) if str(v["value"]).replace(".", "").lstrip("-").isdigit() else 0 for v in chart_data.values()]
            units  = [v["unit"] for v in chart_data.values()]

            fig = go.Figure(go.Bar(
                x=labels,
                y=values,
                text=[f"{v:.2f} {u}" for v, u in zip(values, units)],
                textposition="outside",
                marker=dict(
                    color=["rgba(30,144,255,0.8)", "rgba(0,212,170,0.8)", "rgba(255,183,77,0.8)"],
                    line=dict(color=["#1e90ff", "#00d4aa", "#ffb74d"], width=1.5),
                ),
            ))
            fig.update_layout(
                paper_bgcolor="#0d1b2a",
                plot_bgcolor="#1a2535",
                font=dict(color="#e8edf2", size=12),
                xaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8ca0b5")),
                yaxis=dict(gridcolor="rgba(255,255,255,0.05)", tickfont=dict(color="#8ca0b5"), title="Magnitude"),
                margin=dict(l=40, r=20, t=20, b=40),
                height=320,
            )
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    # ── Exports ──
    st.markdown("### 📤 Export Report")
    ecol1, ecol2 = st.columns(2)

    # PDF
    with ecol1:
        try:
            from reportlab.lib.pagesizes import letter
            from reportlab.lib import colors as rl_colors
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.units import inch as rl_inch
            from reportlab.platypus import (
                SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
            )

            buf = io.BytesIO()
            doc = SimpleDocTemplate(buf, pagesize=letter,
                leftMargin=0.75*rl_inch, rightMargin=0.75*rl_inch,
                topMargin=0.75*rl_inch,  bottomMargin=0.75*rl_inch)
            styles = getSampleStyleSheet()
            navy  = rl_colors.HexColor("#0d1b2a")
            blue  = rl_colors.HexColor("#1e90ff")

            title_s = ParagraphStyle("T", parent=styles["Title"], textColor=navy, fontSize=18, spaceAfter=4)
            sub_s   = ParagraphStyle("S", parent=styles["Normal"], textColor=blue, fontSize=9, spaceAfter=12)
            h2_s    = ParagraphStyle("H", parent=styles["Heading2"], textColor=navy, fontSize=12, spaceBefore=12, spaceAfter=6)
            thin    = lambda c: (0.4, c)

            story = [
                Paragraph("Helical Gear Calculation Report", title_s),
                Paragraph("PD-Based Method  ·  Inch Units  ·  Engineering Grade", sub_s),
                HRFlowable(width="100%", thickness=1, color=blue),
                Spacer(1, 10),
                Paragraph("Input Parameters", h2_s),
            ]

            input_labels = {
                "pitch_diameter": ("Pitch Diameter (PD)", "in"),
                "num_teeth":      ("Number of Teeth (Z)", "—"),
                "helix_angle":    ("Helix Angle (β)",     "°"),
                "pressure_angle": ("Pressure Angle (φ)",  "°"),
                "face_width":     ("Face Width (F)",       "in"),
                "power":          ("Input Power (HP)",     "HP"),
                "rpm":            ("Rotational Speed",     "RPM"),
                "pinion_teeth":   ("Pinion Teeth (Z₁)",   "—"),
                "gear_teeth":     ("Gear Teeth (Z₂)",     "—"),
                "service_factor": ("Service Factor (Ks)",  "—"),
            }
            in_data = [["Parameter", "Value", "Unit"]]
            for key, (lbl, unit) in input_labels.items():
                in_data.append([lbl, str(parsed.get(key, "N/A")), unit])

            ts = TableStyle([
                ("BACKGROUND",   (0,0),(-1,0), navy),
                ("TEXTCOLOR",    (0,0),(-1,0), rl_colors.white),
                ("FONTNAME",     (0,0),(-1,0), "Helvetica-Bold"),
                ("FONTSIZE",     (0,0),(-1,-1), 9),
                ("ROWBACKGROUNDS",(0,1),(-1,-1), [rl_colors.HexColor("#f0f4f8"), rl_colors.white]),
                ("GRID",         (0,0),(-1,-1), 0.4, rl_colors.HexColor("#cccccc")),
                ("PADDING",      (0,0),(-1,-1), 5),
            ])
            story.append(Table(in_data, colWidths=[3.5*rl_inch, 2*rl_inch, 1.2*rl_inch], style=ts))
            story += [Spacer(1, 14), Paragraph("Calculation Results", h2_s)]

            res_data = [["Parameter", "Value", "Unit", "Formula"]]
            for r in results.values():
                res_data.append([r["label"], str(r["value"]), r["unit"], r["formula"]])
            ts2 = TableStyle([
                ("BACKGROUND",    (0,0),(-1,0), blue),
                ("TEXTCOLOR",     (0,0),(-1,0), rl_colors.white),
                ("FONTNAME",      (0,0),(-1,0), "Helvetica-Bold"),
                ("FONTSIZE",      (0,0),(-1,-1), 8),
                ("ROWBACKGROUNDS",(0,1),(-1,-1), [rl_colors.HexColor("#eaf4ff"), rl_colors.white]),
                ("GRID",          (0,0),(-1,-1), 0.4, rl_colors.HexColor("#aaaaaa")),
                ("PADDING",       (0,0),(-1,-1), 5),
            ])
            story.append(Table(res_data, colWidths=[2.3*rl_inch, 1.2*rl_inch, 0.9*rl_inch, 2.3*rl_inch], style=ts2))

            if warnings:
                story += [Spacer(1, 12), Paragraph("Engineering Warnings", h2_s)]
                for w in warnings:
                    story.append(Paragraph(f"⚠  {w}", styles["Normal"]))
                    story.append(Spacer(1, 4))

            story += [
                Spacer(1, 18),
                HRFlowable(width="100%", thickness=0.5, color=rl_colors.grey),
                Paragraph("Generated by Helical Gear Calculator · PD-Based Method · All dimensions in inches",
                           ParagraphStyle("ft", parent=styles["Normal"], fontSize=7, textColor=rl_colors.grey))
            ]
            doc.build(story)
            buf.seek(0)
            st.download_button("📄 Download PDF Report", buf, "helical_gear_report.pdf", "application/pdf", use_container_width=True)
        except ImportError:
            st.warning("ReportLab not installed. Run: `pip install reportlab`")

    # Excel
    with ecol2:
        try:
            import openpyxl
            from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
            from openpyxl.utils import get_column_letter

            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = "Gear Report"

            navy_fill  = PatternFill("solid", fgColor="0D1B2A")
            blue_fill  = PatternFill("solid", fgColor="1E90FF")
            light_fill = PatternFill("solid", fgColor="EAF4FF")
            alt_fill   = PatternFill("solid", fgColor="F0F4F8")
            wf = Font(color="FFFFFF", bold=True)
            thin_b = Border(
                left=Side(style="thin", color="CCCCCC"),
                right=Side(style="thin", color="CCCCCC"),
                top=Side(style="thin", color="CCCCCC"),
                bottom=Side(style="thin", color="CCCCCC"),
            )

            def xhdr(r, c, text, fill):
                cell = ws.cell(row=r, column=c, value=text)
                cell.fill = fill; cell.font = wf
                cell.alignment = Alignment(horizontal="center", vertical="center")
                cell.border = thin_b

            def xcell(r, c, text, fill=None):
                cell = ws.cell(row=r, column=c, value=text)
                if fill: cell.fill = fill
                cell.alignment = Alignment(vertical="center", wrap_text=True)
                cell.border = thin_b

            ws.merge_cells("A1:E1")
            ws["A1"].value = "Helical Gear Calculation Report — PD-Based Method (Inch Units)"
            ws["A1"].font = Font(size=13, bold=True, color="0D1B2A")
            ws["A1"].alignment = Alignment(horizontal="center")
            ws.row_dimensions[1].height = 26

            r = 3
            for c_idx, txt in enumerate(["Parameter", "Value", "Unit"], 1):
                xhdr(r, c_idx, txt, navy_fill)
            r += 1
            input_labels = {
                "pitch_diameter": ("Pitch Diameter (PD)", "in"),
                "num_teeth":      ("Number of Teeth (Z)", "—"),
                "helix_angle":    ("Helix Angle (β)",     "°"),
                "pressure_angle": ("Pressure Angle (φ)",  "°"),
                "face_width":     ("Face Width (F)",       "in"),
                "power":          ("Input Power (HP)",     "HP"),
                "rpm":            ("Rotational Speed",     "RPM"),
                "pinion_teeth":   ("Pinion Teeth (Z₁)",   "—"),
                "gear_teeth":     ("Gear Teeth (Z₂)",     "—"),
                "service_factor": ("Service Factor (Ks)",  "—"),
            }
            for i, (key, (lbl, unit)) in enumerate(input_labels.items()):
                fl = alt_fill if i % 2 == 0 else None
                xcell(r, 1, lbl, fl); xcell(r, 2, parsed.get(key, "N/A"), fl); xcell(r, 3, unit, fl)
                r += 1

            r += 1
            for c_idx, txt in enumerate(["Parameter", "Value", "Unit", "Formula", "Description"], 1):
                xhdr(r, c_idx, txt, blue_fill)
            r += 1
            for i, res_r in enumerate(results.values()):
                fl = light_fill if i % 2 == 0 else None
                xcell(r, 1, res_r["label"], fl); xcell(r, 2, res_r["value"], fl)
                xcell(r, 3, res_r["unit"],  fl); xcell(r, 4, res_r["formula"], fl)
                xcell(r, 5, res_r["description"], fl)
                r += 1

            for col, width in zip("ABCDE", [32, 14, 10, 45, 50]):
                ws.column_dimensions[col].width = width

            xbuf = io.BytesIO()
            wb.save(xbuf); xbuf.seek(0)
            st.download_button("📊 Download Excel Report", xbuf, "helical_gear_report.xlsx",
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True)
        except ImportError:
            st.warning("openpyxl not installed. Run: `pip install openpyxl`")

else:
    # ── Placeholder ──
    st.markdown("""
    <div style="
        display:flex; flex-direction:column; align-items:center; justify-content:center;
        min-height:320px; color:#8ca0b5; text-align:center; gap:12px;
        background:rgba(30,45,61,0.4); border:1px solid rgba(30,144,255,0.12);
        border-radius:14px; padding:40px;
    ">
      <div style="font-size:60px; opacity:0.3">⚙</div>
      <div style="font-size:1.3rem; font-weight:700; opacity:0.55">Awaiting Calculation</div>
      <div style="font-size:0.85rem; opacity:0.4; max-width:340px;">
        Fill in the input parameters in the sidebar, select your desired outputs, then click <strong>⚡ Calculate</strong>.
      </div>
    </div>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
# Formula Reference (always visible)
# ─────────────────────────────────────────────
st.markdown("---")
with st.expander("📖 Formula Reference — PD-Based Method (Inch Units)", expanded=False):
    formulas = [
        ("Diametral Pitch",        "DP = Z / PD",                          "Teeth per inch of pitch diameter. Defines tooth size."),
        ("Circular Pitch",         "CP = π / DP = π·PD / Z",               "Arc length between corresponding points of adjacent teeth."),
        ("Transverse Pressure Angle","tan(φₜ) = tan(φₙ) / cos(β)",        "Derived from normal pressure angle and helix angle."),
        ("Base Circle Diameter",   "BCD = PD · cos(φₜ)",                   "Diameter of the involute base circle in the transverse plane."),
        ("Outside Diameter",       "OD = PD + 2/DP",                       "Addendum = 1/DP. Total outer diameter of the gear."),
        ("Root Diameter",          "RD = PD − 2.5/DP",                     "Dedendum = 1.25/DP (standard full depth). Diameter at tooth root."),
        ("Lead",                   "L = π·PD / tan(β)",                    "Axial advance per one full revolution of the helix."),
        ("Gear Ratio",             "GR = Z₂ / Z₁",                         "Speed reduction ratio from pinion (Z₁) to gear (Z₂)."),
        ("Torque",                 "T = HP × 63,025 / RPM",                "Driving torque in lb·in. Constant 63,025 = 33,000×12/(2π)."),
        ("Tangential Force",       "Wₜ = (2T / PD) × Ks",                 "Tangential tooth load in lbf, scaled by service factor."),
        ("Axial Force",            "Wₐ = Wₜ · tan(β)",                    "Axial (thrust) force component due to helix angle."),
        ("Normal Diametral Pitch", "DPₙ = DP / cos(β)",                    "Diametral pitch in the normal plane (for tool selection)."),
    ]
    cols = st.columns(2)
    for i, (name, eq, desc) in enumerate(formulas):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="formula-card">
              <div class="fc-name">{name}</div>
              <div class="fc-eq">{eq}</div>
              <div class="fc-desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="font-size:0.78rem; color:#8ca0b5; line-height:1.7; margin-top:0.5rem; padding:12px 16px; background:#1e2d3d; border-radius:8px;">
    <strong style="color:#8ca0b5">Engineering Assumptions:</strong>
    Standard full-depth tooth profile (AGMA/ANSI) — Addendum = 1/DP, Dedendum = 1.25/DP.
    Normal pressure angle is the input; transverse pressure angle is derived internally.
    Service factor is applied directly to tangential force.
    Torque constant 63,025 assumes HP, RPM, and lb·in units.
    All dimensions in <strong>inches (in)</strong>.
    </div>
    """, unsafe_allow_html=True)
