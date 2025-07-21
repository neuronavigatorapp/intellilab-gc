def build():
    from pathlib import Path
    import textwrap

    path = Path("utils/pdf_export.py")
    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(textwrap.dedent("""
        import os
        import pandas as pd
        from matplotlib import pyplot as plt
        from fpdf import FPDF
        from pathlib import Path

        def export_simulation_report(peaks: list, faults: list, fig):
            export_dir = Path("exports")
            export_dir.mkdir(exist_ok=True)
            image_path = export_dir / "chromatogram.png"
            pdf_path = export_dir / "simulation_report.pdf"

            # Save chromatogram image
            fig.savefig(image_path, dpi=150)

            # Convert peak table to DataFrame and CSV (optional)
            df = pd.DataFrame(peaks)
            table_csv = export_dir / "peak_table.csv"
            df.to_csv(table_csv, index=False)

            # Generate PDF
            pdf = FPDF()
            pdf.add_page()

            pdf.set_font("Arial", "B", 16)
            pdf.cell(0, 10, "IntelliLab GC Simulation Report", ln=True)

            pdf.set_font("Arial", "", 12)
            pdf.cell(0, 10, f"Faults: {', '.join(faults) if faults else 'None'}", ln=True)
            pdf.ln(5)

            # Insert chromatogram image
            pdf.image(str(image_path), w=180)
            pdf.ln(10)

            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 10, "Peak Table (first 8 shown):", ln=True)

            # Table header
            pdf.set_font("Arial", "", 10)
            for i, row in df.head(8).iterrows():
                row_str = f"{row['name']} | RT: {row['rt']} | Area: {row['area']} | Height: {row['height']} | Width: {row['width']}"
                pdf.cell(0, 8, row_str, ln=True)

            pdf.output(str(pdf_path))
            return str(pdf_path)
    """))

    print("Patch 045 applied: Simulated run PDF export added.")
    return [], [], []

if __name__ == "__main__":
    build()
