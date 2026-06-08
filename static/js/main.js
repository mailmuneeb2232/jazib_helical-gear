/* ============================================================
   Helical Gear Calculator — Frontend Logic
   ============================================================ */

"use strict";

// --------------------------------------------------------------------------
// Constants
// --------------------------------------------------------------------------

const OUTPUT_DEFS = [
  { key: "diametral_pitch",      label: "Diametral Pitch",       icon: "⚙" },
  { key: "circular_pitch",       label: "Circular Pitch",        icon: "⭕" },
  { key: "base_circle_diameter", label: "Base Circle Dia.",      icon: "🔵" },
  { key: "outside_diameter",     label: "Outside Diameter",      icon: "📐" },
  { key: "root_diameter",        label: "Root Diameter",         icon: "📏" },
  { key: "lead",                 label: "Lead",                  icon: "↕" },
  { key: "gear_ratio",           label: "Gear Ratio",            icon: "⚖" },
  { key: "tangential_force",     label: "Tangential Force",      icon: "➡" },
  { key: "axial_force",          label: "Axial Force",           icon: "⬆" },
  { key: "torque",               label: "Torque",                icon: "🔄" },
];

const INPUT_RULES = {
  pitch_diameter:  { min: 0.1,   max: 200,    label: "Pitch Diameter" },
  num_teeth:       { min: 6,     max: 500,    label: "Number of Teeth", integer: true },
  helix_angle:     { min: 1,     max: 89,     label: "Helix Angle" },
  pressure_angle:  { min: 1,     max: 45,     label: "Pressure Angle" },
  face_width:      { min: 0.01,  max: 100,    label: "Face Width" },
  power:           { min: 0.001, max: 100000, label: "Input Power" },
  rpm:             { min: 1,     max: 100000, label: "RPM" },
  pinion_teeth:    { min: 6,     max: 500,    label: "Pinion Teeth", integer: true },
  gear_teeth:      { min: 6,     max: 500,    label: "Gear Teeth", integer: true },
  service_factor:  { min: 0.5,   max: 5,      label: "Service Factor" },
};

// Chart instance
let forceChart = null;

// --------------------------------------------------------------------------
// Initialisation
// --------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", () => {
  buildOutputToggles();
  attachInputValidators();
  attachMainActions();
  attachModalHandlers();
});

// --------------------------------------------------------------------------
// Output toggles
// --------------------------------------------------------------------------

function buildOutputToggles() {
  const grid = document.getElementById("outputGrid");
  OUTPUT_DEFS.forEach(def => {
    const label = document.createElement("label");
    label.className = "output-toggle";
    label.dataset.key = def.key;
    label.innerHTML = `
      <input type="checkbox" value="${def.key}">
      <span class="toggle-check">✓</span>
      <span>${def.icon} ${def.label}</span>
    `;
    label.addEventListener("click", () => {
      label.classList.toggle("selected");
      const cb = label.querySelector("input");
      cb.checked = !cb.checked;
    });
    grid.appendChild(label);
  });
}

function getSelectedOutputs() {
  return [...document.querySelectorAll(".output-toggle.selected")]
    .map(el => el.dataset.key);
}

function selectAllOutputs() {
  document.querySelectorAll(".output-toggle").forEach(el => {
    el.classList.add("selected");
    el.querySelector("input").checked = true;
  });
}

function clearAllOutputs() {
  document.querySelectorAll(".output-toggle").forEach(el => {
    el.classList.remove("selected");
    el.querySelector("input").checked = false;
  });
}

// --------------------------------------------------------------------------
// Input validation
// --------------------------------------------------------------------------

function attachInputValidators() {
  Object.keys(INPUT_RULES).forEach(key => {
    const input = document.getElementById(key);
    if (!input) return;
    input.addEventListener("input", () => validateField(key, input));
    input.addEventListener("blur",  () => validateField(key, input));
  });
}

function validateField(key, input) {
  const rule = INPUT_RULES[key];
  const errEl = document.getElementById(`err_${key}`);
  const raw = input.value.trim();

  if (raw === "") {
    setFieldState(input, errEl, null, "");
    return true;
  }

  const num = Number(raw);
  if (isNaN(num)) {
    setFieldState(input, errEl, false, "Must be a valid number.");
    return false;
  }
  if (rule.integer && !Number.isInteger(num)) {
    setFieldState(input, errEl, false, "Must be a whole number.");
    return false;
  }
  if (num < rule.min || num > rule.max) {
    setFieldState(input, errEl, false, `Range: ${rule.min} – ${rule.max}`);
    return false;
  }
  setFieldState(input, errEl, true, "");
  return true;
}

function setFieldState(input, errEl, valid, msg) {
  input.classList.toggle("invalid", valid === false);
  input.classList.toggle("valid",   valid === true);
  if (errEl) {
    errEl.textContent = msg;
    errEl.classList.toggle("show", !!msg);
  }
}

function getInputValues() {
  const vals = {};
  Object.keys(INPUT_RULES).forEach(key => {
    const el = document.getElementById(key);
    if (el) vals[key] = el.value.trim();
  });
  return vals;
}

// --------------------------------------------------------------------------
// Main actions
// --------------------------------------------------------------------------

function attachMainActions() {
  document.getElementById("btnCalculate").addEventListener("click", runCalculation);
  document.getElementById("btnSelectAll").addEventListener("click", selectAllOutputs);
  document.getElementById("btnClearAll").addEventListener("click", clearAllOutputs);
  document.getElementById("btnReset").addEventListener("click", resetForm);
  document.getElementById("btnExportPDF").addEventListener("click", () => exportReport("pdf"));
  document.getElementById("btnExportExcel").addEventListener("click", () => exportReport("excel"));
}

async function runCalculation() {
  const btn = document.getElementById("btnCalculate");
  const selected = getSelectedOutputs();

  if (!selected.length) {
    showToast("Please select at least one output parameter.", "warning");
    return;
  }

  // Validate all inputs
  let valid = true;
  Object.keys(INPUT_RULES).forEach(key => {
    const inp = document.getElementById(key);
    if (inp && !validateField(key, inp)) valid = false;
  });
  if (!valid) {
    showToast("Please fix the highlighted input errors.", "error");
    return;
  }

  btn.classList.add("loading");
  btn.innerHTML = `<span class="spinner"></span> Calculating…`;

  try {
    const res = await fetch("/calculate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs: getInputValues(), selected_outputs: selected }),
    });

    const data = await res.json();

    if (!res.ok) {
      if (data.errors) showErrors(data.errors);
      else if (data.error) showToast(data.error, "error");
      return;
    }

    renderResults(data);
    showToast("Calculation complete!", "success");
  } catch (e) {
    showToast("Network error — please try again.", "error");
  } finally {
    btn.classList.remove("loading");
    btn.innerHTML = `⚡ Calculate`;
  }
}

// --------------------------------------------------------------------------
// Render results
// --------------------------------------------------------------------------

function renderResults({ results, warnings }) {
  const zone = document.getElementById("resultsZone");
  zone.innerHTML = "";

  // Export bar
  const exportBar = document.createElement("div");
  exportBar.className = "export-bar";
  exportBar.innerHTML = `
    <span class="label">Export:</span>
    <button class="btn btn-success btn-sm" onclick="exportReport('pdf')">📄 PDF Report</button>
    <button class="btn btn-teal btn-sm" onclick="exportReport('excel')">📊 Excel Report</button>
    <button class="btn btn-ghost btn-sm" onclick="window.print()">🖨 Print</button>
  `;
  zone.appendChild(exportBar);

  // Warnings
  if (warnings && warnings.length) {
    const wb = document.createElement("div");
    wb.className = "warning-banner";
    wb.innerHTML = `
      <div class="warn-title">⚠ Engineering Warnings</div>
      <ul>${warnings.map(w => `<li>${w}</li>`).join("")}</ul>
    `;
    zone.appendChild(wb);
  }

  // Metric cards
  const grid = document.createElement("div");
  grid.className = "metrics-grid";
  Object.values(results).forEach((r, idx) => {
    const card = document.createElement("div");
    card.className = "metric-card";
    card.style.animationDelay = `${idx * 0.05}s`;
    card.innerHTML = `
      <div class="metric-label">${r.label}</div>
      <div class="metric-value">${r.value}</div>
      <div class="metric-unit">${r.unit}</div>
      <div class="metric-formula">${escHtml(r.formula)}</div>
    `;
    grid.appendChild(card);
  });
  zone.appendChild(grid);

  // Summary table card
  const tableCard = document.createElement("div");
  tableCard.className = "card";
  tableCard.innerHTML = `
    <div class="card-header">
      <div class="icon">📋</div>
      <h3>Engineering Summary</h3>
    </div>
    <div class="card-body" style="padding:0">
      <div class="results-table-wrap">
        <table class="results-table">
          <thead>
            <tr>
              <th>Parameter</th>
              <th>Value</th>
              <th>Unit</th>
              <th>Formula</th>
              <th>Description</th>
            </tr>
          </thead>
          <tbody>
            ${Object.values(results).map(r => `
              <tr>
                <td><strong>${r.label}</strong></td>
                <td class="val-cell">${r.value}</td>
                <td><span class="badge-unit">${r.unit}</span></td>
                <td class="formula-cell">${escHtml(r.formula)}</td>
                <td style="font-size:0.78rem;color:var(--text-muted)">${r.description}</td>
              </tr>
            `).join("")}
          </tbody>
        </table>
      </div>
    </div>
  `;
  zone.appendChild(tableCard);

  // Chart (forces + torque if available)
  buildChart(zone, results);

  // Scroll into view
  zone.scrollIntoView({ behavior: "smooth", block: "start" });
}

function buildChart(zone, results) {
  const chartKeys  = ["tangential_force", "axial_force", "torque"];
  const available  = chartKeys.filter(k => results[k]);
  if (!available.length) return;

  const chartCard = document.createElement("div");
  chartCard.className = "card";
  chartCard.innerHTML = `
    <div class="card-header">
      <div class="icon">📈</div>
      <h3>Force & Torque Visualization</h3>
    </div>
    <div class="card-body">
      <div class="chart-container">
        <canvas id="forceChart"></canvas>
      </div>
    </div>
  `;
  zone.appendChild(chartCard);

  const labels = available.map(k => results[k].label);
  const values = available.map(k => Number(results[k].value) || 0);
  const units  = available.map(k => results[k].unit);

  if (forceChart) forceChart.destroy();
  const ctx = document.getElementById("forceChart").getContext("2d");
  forceChart = new Chart(ctx, {
    type: "bar",
    data: {
      labels,
      datasets: [{
        label: "Value",
        data: values,
        backgroundColor: [
          "rgba(30,144,255,0.7)",
          "rgba(0,212,170,0.7)",
          "rgba(255,183,77,0.7)",
        ],
        borderColor: [
          "rgba(30,144,255,1)",
          "rgba(0,212,170,1)",
          "rgba(255,183,77,1)",
        ],
        borderWidth: 1.5,
        borderRadius: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => {
              const u = units[ctx.dataIndex];
              return ` ${ctx.parsed.y.toLocaleString()} ${u}`;
            },
          },
          backgroundColor: "#1e2d3d",
          titleColor: "#e8edf2",
          bodyColor: "#8ca0b5",
          borderColor: "rgba(30,144,255,0.3)",
          borderWidth: 1,
        },
      },
      scales: {
        x: {
          ticks: { color: "#8ca0b5", font: { size: 11 } },
          grid: { color: "rgba(255,255,255,0.05)" },
        },
        y: {
          ticks: { color: "#8ca0b5", font: { size: 11 } },
          grid: { color: "rgba(255,255,255,0.05)" },
          title: {
            display: true,
            text: "Magnitude",
            color: "#8ca0b5",
            font: { size: 11 },
          },
        },
      },
    },
  });
}

// --------------------------------------------------------------------------
// Error rendering
// --------------------------------------------------------------------------

function showErrors(errors) {
  const zone = document.getElementById("resultsZone");
  zone.innerHTML = `
    <div class="error-banner">
      <strong style="color:var(--danger)">⛔ Validation Errors</strong>
      <ul>${errors.map(e => `<li>${e}</li>`).join("")}</ul>
    </div>
  `;
}

// --------------------------------------------------------------------------
// Export
// --------------------------------------------------------------------------

async function exportReport(format) {
  const selected = getSelectedOutputs();
  if (!selected.length) { showToast("Select outputs before exporting.", "warning"); return; }

  showToast(`Generating ${format.toUpperCase()} report…`, "success");

  try {
    const res = await fetch(`/export/${format}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ inputs: getInputValues(), selected_outputs: selected }),
    });

    if (!res.ok) {
      const d = await res.json();
      showToast(d.error || "Export failed.", "error");
      return;
    }

    const blob = await res.blob();
    const url  = URL.createObjectURL(blob);
    const a    = document.createElement("a");
    a.href = url;
    a.download = format === "pdf" ? "helical_gear_report.pdf" : "helical_gear_report.xlsx";
    a.click();
    URL.revokeObjectURL(url);
    showToast(`${format.toUpperCase()} downloaded!`, "success");
  } catch {
    showToast("Export error — please try again.", "error");
  }
}

// --------------------------------------------------------------------------
// Save / Load
// --------------------------------------------------------------------------

function attachModalHandlers() {
  // Save
  document.getElementById("btnSave").addEventListener("click", () => {
    const payload = JSON.stringify({ inputs: getInputValues(), outputs: getSelectedOutputs() }, null, 2);
    document.getElementById("saveData").value = payload;
    document.getElementById("saveModal").classList.remove("hidden");
  });
  document.getElementById("btnSaveClose").addEventListener("click",  () => document.getElementById("saveModal").classList.add("hidden"));
  document.getElementById("btnSaveCopy").addEventListener("click", () => {
    navigator.clipboard.writeText(document.getElementById("saveData").value);
    showToast("Copied to clipboard!", "success");
  });
  document.getElementById("btnSaveDownload").addEventListener("click", () => {
    const blob = new Blob([document.getElementById("saveData").value], { type: "application/json" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = "gear_project.json";
    a.click();
    showToast("Project saved!", "success");
  });

  // Load
  document.getElementById("btnLoad").addEventListener("click", () => {
    document.getElementById("loadModal").classList.remove("hidden");
  });
  document.getElementById("btnLoadClose").addEventListener("click", () => document.getElementById("loadModal").classList.add("hidden"));
  document.getElementById("btnLoadFile").addEventListener("click", () => document.getElementById("loadFileInput").click());
  document.getElementById("loadFileInput").addEventListener("change", e => {
    const f = e.target.files[0];
    if (!f) return;
    const reader = new FileReader();
    reader.onload = ev => { document.getElementById("loadData").value = ev.target.result; };
    reader.readAsText(f);
  });
  document.getElementById("btnLoadApply").addEventListener("click", () => {
    try {
      const data = JSON.parse(document.getElementById("loadData").value);
      if (data.inputs) {
        Object.entries(data.inputs).forEach(([k, v]) => {
          const el = document.getElementById(k);
          if (el) el.value = v;
        });
      }
      if (data.outputs) {
        clearAllOutputs();
        data.outputs.forEach(key => {
          const toggle = document.querySelector(`.output-toggle[data-key="${key}"]`);
          if (toggle) { toggle.classList.add("selected"); toggle.querySelector("input").checked = true; }
        });
      }
      document.getElementById("loadModal").classList.add("hidden");
      showToast("Project loaded successfully!", "success");
    } catch {
      showToast("Invalid JSON — check your file.", "error");
    }
  });
}

// --------------------------------------------------------------------------
// Reset
// --------------------------------------------------------------------------

function resetForm() {
  document.querySelectorAll(".input-wrap input").forEach(inp => {
    inp.value = "";
    inp.classList.remove("valid", "invalid");
  });
  document.querySelectorAll(".field-error").forEach(el => {
    el.textContent = "";
    el.classList.remove("show");
  });
  clearAllOutputs();
  document.getElementById("resultsZone").innerHTML = `
    <div class="results-placeholder">
      <div class="big-icon">⚙</div>
      <h2>Awaiting Calculation</h2>
      <p>Fill in the input parameters on the left, select your desired outputs, then click <strong>Calculate</strong>.</p>
    </div>
  `;
  if (forceChart) { forceChart.destroy(); forceChart = null; }
  showToast("Form reset.", "success");
}

// --------------------------------------------------------------------------
// Toast notifications
// --------------------------------------------------------------------------

function showToast(msg, type = "success") {
  const container = document.getElementById("toastContainer");
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  const icon = { success: "✅", warning: "⚠", error: "❌" }[type] || "ℹ";
  toast.innerHTML = `<span>${icon}</span><span>${msg}</span>`;
  container.appendChild(toast);
  setTimeout(() => { toast.style.opacity = "0"; toast.style.transform = "translateX(40px)"; toast.style.transition = "all 0.3s"; setTimeout(() => toast.remove(), 300); }, 3500);
}

// --------------------------------------------------------------------------
// Utility
// --------------------------------------------------------------------------

function escHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");
}
