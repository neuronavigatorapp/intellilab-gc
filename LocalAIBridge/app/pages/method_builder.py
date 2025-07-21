import streamlit as st
import pandas as pd
import os
import json

METHOD_FILE = "data/methods.json"

def load_methods():
    if os.path.exists(METHOD_FILE):
        with open(METHOD_FILE, "r") as f:
            return json.load(f)
    return []

def save_methods(methods):
    with open(METHOD_FILE, "w") as f:
        json.dump(methods, f, indent=2)

def main():
    st.title("GC Method Builder")

    methods = load_methods()

    with st.form("method_form"):
        name = st.text_input("Method Name")
        column = st.text_input("Column Type (e.g., DB-1, DB-5)")
        gas = st.selectbox("Carrier Gas", ["Helium", "Nitrogen", "Hydrogen"])
        temp_start = st.number_input("Oven Start Temp (°C)", step=1)
        temp_end = st.number_input("Oven End Temp (°C)", step=1)
        ramp = st.number_input("Ramp Rate (°C/min)", step=0.1)
        split = st.number_input("Split Ratio", step=0.1)
        detector = st.selectbox("Detector Type", ["FID", "TCD", "ECD", "MSD"])
        submitted = st.form_submit_button("Save Method")

        if submitted:
            methods.append({
                "name": name,
                "column": column,
                "gas": gas,
                "start_temp": temp_start,
                "end_temp": temp_end,
                "ramp": ramp,
                "split": split,
                "detector": detector
            })
            save_methods(methods)
            st.success("Method saved successfully.")

    if methods:
        st.subheader("Saved Methods")
        df = pd.DataFrame(methods)
        st.dataframe(df)

if __name__ == "__main__":
    main()
