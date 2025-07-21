import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from utils.chromatogram_generator import generate_peaks
from utils.fault_toggles import load_fault_config, save_fault_config
from utils.ai_diagnosis import diagnose_issues
from utils.run_compare import save_baseline_run, load_baseline_run, has_baseline
from utils.scenario_cards import list_scenarios, load_scenario
from utils.pdf_export import export_simulation_report

st.set_page_config(page_title="GC Simulator", layout="wide")
st.title("Gas Chromatography Simulator")

# Scenario selection
scenarios = list_scenarios()
selected_scenario = st.selectbox("Load a GC Fault Scenario:", ["None"] + scenarios)

if selected_scenario != "None":
    scenario_data = load_scenario(selected_scenario)
    faults = scenario_data.get("faults", [])
    save_fault_config(faults)
    st.success(f"Loaded scenario: {selected_scenario}")
    st.write("Notes:", scenario_data.get("notes", ""))
else:
    faults = load_fault_config()

st.write(f"Active Faults: {', '.join(faults) if faults else 'None'}")

# Generate simulated chromatogram
sim_peaks = generate_peaks(
    faults=faults,
    shift_rt="inlet_leak" in faults,
    baseline_noise="baseline_noise" in faults,
    coelution="coelution" in faults
)

# Save simulated run as baseline
if st.button("📥 Save This Run as Baseline"):
    save_baseline_run(sim_peaks)
    st.success("Baseline chromatogram saved.")

# Display peak tables
if has_baseline():
    baseline_peaks = load_baseline_run()
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Baseline Peak Table")
        st.dataframe(baseline_peaks)
    with col2:
        st.subheader("Simulated Peak Table")
        st.dataframe(sim_peaks)
else:
    st.subheader("Simulated Peak Table")
    st.dataframe(sim_peaks)

# Chromatogram plot
st.subheader("Chromatogram Comparison")
fig, ax = plt.subplots(figsize=(10, 4))

def plot_peaks(peaks, label_suffix="", color=None, linestyle="-"):
    for peak in peaks:
        rt = peak["rt"]
        height = peak["height"]
        width = peak["width"]
        label = f"{peak['name']} {label_suffix}"
        x = np.linspace(rt - width * 2.5, rt + width * 2.5, 200)
        y = height * np.exp(-((x - rt) ** 2) / (2 * (width / 2.355) ** 2))
        ax.plot(x, y, label=label, color=color, linestyle=linestyle)

if has_baseline():
    plot_peaks(baseline_peaks, label_suffix="(Baseline)", color="blue", linestyle="--")
plot_peaks(sim_peaks, label_suffix="(Simulated)", color="red")

ax.set_xlabel("Retention Time (min)")
ax.set_ylabel("Detector Signal")
ax.legend(loc="upper right", fontsize="small")
ax.grid(True)
st.pyplot(fig)

# Export to PDF
if st.button("📤 Export PDF Report"):
    pdf_path = export_simulation_report(sim_peaks, faults, fig)
    st.success("PDF report created.")
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📄 Download Simulation Report",
            data=f,
            file_name="gc_simulation_report.pdf",
            mime="application/pdf"
        )

# AI Troubleshooting
st.subheader("AI Diagnostic Suggestions")
diagnostics = diagnose_issues(sim_peaks, faults)
for tip in diagnostics:
    st.markdown(f"- {tip}")
