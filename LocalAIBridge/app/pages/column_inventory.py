import streamlit as st
import json
import os
import pandas as pd

COLUMN_FILE = "data/columns.json"
METHOD_FILE = "data/methods.json"

def load_columns():
    if os.path.exists(COLUMN_FILE):
        with open(COLUMN_FILE, "r") as f:
            return json.load(f)
    return []

def save_columns(columns):
    with open(COLUMN_FILE, "w") as f:
        json.dump(columns, f, indent=2)

def load_methods():
    if os.path.exists(METHOD_FILE):
        with open(METHOD_FILE, "r") as f:
            return json.load(f)
    return []

def check_compatibility(column, methods):
    issues = []
    for method in methods:
        if column["max_temp"] < method["end_temp"]:
            issues.append(f"⚠️ '{method['name']}' exceeds max temp ({column['max_temp']}°C)")
        if method["column"] and method["column"].lower() not in column["name"].lower():
            issues.append(f"⚠️ Polarity mismatch or column type mismatch with '{method['name']}'")
    return issues

def main():
    st.title("GC Column Inventory & Compatibility")

    columns = load_columns()
    methods = load_methods()

    with st.form("add_column"):
        name = st.text_input("Column Name")
        length = st.number_input("Length (m)", step=0.1)
        id_val = st.number_input("ID (mm)", step=0.01)
        film = st.number_input("Film Thickness (μm)", step=0.01)
        max_temp = st.number_input("Max Temperature (°C)", step=1)
        polarity = st.selectbox("Polarity", ["Low", "Medium", "High"])
        submitted = st.form_submit_button("Add Column")

        if submitted:
            columns.append({
                "name": name,
                "length": length,
                "id": id_val,
                "film": film,
                "max_temp": max_temp,
                "polarity": polarity
            })
            save_columns(columns)
            st.success("Column saved successfully.")
            st.experimental_rerun()

    if columns:
        st.subheader("Column Inventory")
        for col in columns:
            st.markdown("""**{}** — {}m × {}mm × {}μm  
Max Temp: {}°C  
Polarity: {}""".format(
                col["name"],
                col["length"],
                col["id"],
                col["film"],
                col["max_temp"],
                col["polarity"]
            ))

            issues = check_compatibility(col, methods)
            for issue in issues:
                st.warning(issue)
            st.markdown("---")

if __name__ == "__main__":
    main()
