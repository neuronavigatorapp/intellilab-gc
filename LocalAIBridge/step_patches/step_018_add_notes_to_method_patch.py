import os

def build():
    path_builder = "app/pages/method_builder.py"
    path_preview = "app/pages/method_preview.py"
    os.makedirs(os.path.dirname(path_builder), exist_ok=True)

    with open(path_builder, "a", encoding="utf-8") as f:
        f.write("""\n    # Notes section\n    notes = st.text_area("Method Notes")\n""")
        f.write("""\n        if submitted:\n            methods.append({\n                "name": name,\n                "column": column,\n                "gas": gas,\n                "start_temp": temp_start,\n                "end_temp": temp_end,\n                "ramp": ramp,\n                "split": split,\n                "detector": detector,\n                "notes": notes\n            })\n""")

    with open(path_preview, "a", encoding="utf-8") as f:
        f.write("""\n        st.subheader("Method Notes")\n        st.markdown(method.get("notes", "No notes available."))\n""")
        f.write("""\n        pdf.cell(200, 10, txt="Notes:", ln=True)\n        pdf.multi_cell(0, 10, method_dict.get("notes", "No notes provided."))\n""")

    return [path_builder, path_preview]
