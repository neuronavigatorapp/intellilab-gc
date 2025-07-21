import streamlit as st
import json
import os
import pandas as pd

METHOD_FILE = "data/methods.json"
LINK_FILE = "data/instrument_methods.json"

def load_methods():
    if os.path.exists(METHOD_FILE):
        with open(METHOD_FILE, "r") as f:
            return json.load(f)
    return []

def load_links():
    if os.path.exists(LINK_FILE):
        with open(LINK_FILE, "r") as f:
            return json.load(f)
    return []

def save_links(links):
    with open(LINK_FILE, "w") as f:
        json.dump(links, f, indent=2)

def main():
    st.title("Assign Method to Instrument")

    methods = load_methods()
    links = load_links()

    instrument = st.selectbox("Select Instrument", ["GC-001", "GC-002", "GC-003"])
    method_names = [m["name"] for m in methods]
    if not method_names:
        st.warning("No methods available. Please create one first.")
        return

    method_choice = st.selectbox("Select Method", method_names)

    if st.button("Assign Method"):
        links = [link for link in links if link["instrument"] != instrument]
        links.append({"instrument": instrument, "method": method_choice})
        save_links(links)
        st.success(f"Method '{method_choice}' assigned to {instrument}")

    if links:
        st.subheader("Current Assignments")
        df = pd.DataFrame(links)
        st.dataframe(df)

if __name__ == "__main__":
    main()
