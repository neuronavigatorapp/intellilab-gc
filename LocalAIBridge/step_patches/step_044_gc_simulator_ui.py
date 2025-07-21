def build():
    from pathlib import Path
    import textwrap

    ui_file = Path("app/pages/gc_simulator.py")
    ui_file.parent.mkdir(parents=True, exist_ok=True)

    ui_file.write_text(textwrap.dedent("""
        import streamlit as st
        import matplotlib.pyplot as plt
        from utils.chromatogram_generator import generate_peaks
        from utils.fault_toggles import load_fault_config

        st.set_page_config(page_title="GC Simulator", layout="wide")

        st.title("Gas Chromatography Simulator")

        faults = load_fault_config()
        st.write(f"Active Faults: {', '.join(faults) if faults else 'None'}")

        # Simulate peaks based on faults
        peaks = generate_peaks(
            faults=faults,
            shift_rt="inlet_leak" in faults,
            baseline_noise="baseline_noise" in faults,
            coelution="coelution" in faults
        )

        # Display peak data table
        st.subheader("Simulated Peak Table")
        st.dataframe(peaks)

        # Plot chromatogram
        st.subheader("Chromatogram")
        fig, ax = plt.subplots(figsize=(10, 4))

        for peak in peaks:
            rt = peak["rt"]
            height = peak["height"]
            width = peak["width"]
            label = peak["name"]

            # Generate a Gaussian-like peak
            import numpy as np
            x = np.linspace(rt - width * 2.5, rt + width * 2.5, 200)
            y = height * np.exp(-((x - rt)**2) / (2 * (width / 2.355)**2))
            ax.plot(x, y, label=label)

        ax.set_xlabel("Retention Time (min)")
        ax.set_ylabel("Detector Signal")
        ax.legend(loc="upper right", fontsize="small")
        ax.grid(True)

        st.pyplot(fig)
    """))

    print("Patch 028 applied: GC Simulator visualization UI added.")
    return [], [], []

if __name__ == "__main__":
    build()
