import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

MAINT_FILE = "data/maintenance_log.csv"
METHOD_FILE = "data/instrument_methods.json"
INSTRUMENTS = ["GC-001", "GC-002", "GC-003"]

def load_maintenance():
    if os.path.exists(MAINT_FILE):
        return pd.read_csv(MAINT_FILE, parse_dates=["Date"])
    return pd.DataFrame(columns=["Date", "Instrument", "Action", "By", "Notes"])

def load_assignments():
    if os.path.exists(METHOD_FILE):
        with open(METHOD_FILE, "r") as f:
            return json.load(f)
    return []

def get_method_for(instrument, assignments):
    for a in assignments:
        if a["instrument"] == instrument:
            return a["method"]
    return "Not assigned"

def get_last_maintenance(df, instrument):
    logs = df[df["Instrument"] == instrument].sort_values("Date", ascending=False)
    return logs.iloc[0]["Date"].strftime("%Y-%m-%d") if not logs.empty else "None"

def get_status_color(days):
    if days < 15:
        return "✅ OK"
    elif days < 30:
        return "⚠️ Due Soon"
    else:
        return "🔴 Overdue"

def update_dashboard_widgets(df):
    selected = st.selectbox("Filter by Instrument", ["All"] + INSTRUMENTS, key="instrument_filter")

    if selected != "All":
        df = df[df["Instrument"] == selected]

    st.subheader("Method Assignment Breakdown")
    method_counts = df["Assigned Method"].value_counts()
    st.bar_chart(method_counts)

    st.subheader("Status Distribution")
    status_counts = df["Status"].value_counts()
    st.bar_chart(status_counts)

def main():
    st.title("Instrument Dashboard Overview")

    maint_df = load_maintenance()
    assignments = load_assignments()

    dashboard = []

    for inst in INSTRUMENTS:
        last_date = get_last_maintenance(maint_df, inst)
        method = get_method_for(inst, assignments)

        if last_date != "None":
            days_since = (datetime.today() - pd.to_datetime(last_date)).days
            status = get_status_color(days_since)
        else:
            status = "⚠️ No Record"

        dashboard.append({
            "Instrument": inst,
            "Assigned Method": method,
            "Last Maintenance": last_date,
            "Status": status
        })

    df = pd.DataFrame(dashboard)
    st.dataframe(df)

    update_dashboard_widgets(df)

if __name__ == "__main__":
    main()
