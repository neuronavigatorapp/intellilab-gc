import streamlit as st
import json
import os
import pandas as pd
import plotly.graph_objects as go

METHOD_FILE = "data/methods.json"

def load_methods():
    if os.path.exists(METHOD_FILE):
        with open(METHOD_FILE, "r") as f:
            return json.load(f)
    return []

def main():
    st.title("Method Preview & Parameters")

    methods = load_methods()
    if not methods:
        st.warning("No methods found. Please create one first.")
        return

    selected = st.selectbox("Select a Method", [m["name"] for m in methods])
    method = next((m for m in methods if m["name"] == selected), None)

    if method:
        st.subheader("Method Parameters")
        st.json(method)

        st.subheader("Temperature Program")
        ramp_time = (method["end_temp"] - method["start_temp"]) / method["ramp"]
        x_vals = [0, ramp_time]
        y_vals = [method["start_temp"], method["end_temp"]]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines+markers', name='Oven Temp'))
        fig.update_layout(title="Oven Program", xaxis_title="Time (min)", yaxis_title="Temp (°C)")
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("Detection Setup")
        st.markdown(f"**Detector:** {method['detector']}  \n**Split Ratio:** {method['split']}")
 


if __name__ == "__main__":
    main()
