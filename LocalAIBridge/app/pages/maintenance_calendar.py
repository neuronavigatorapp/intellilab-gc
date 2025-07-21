import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

LOG_FILE = "data/maintenance_log.csv"

def load_logs():
    if os.path.exists(LOG_FILE):
        return pd.read_csv(LOG_FILE, parse_dates=["Date"])
    else:
        return pd.DataFrame(columns=["Date", "Instrument", "Action", "By", "Notes"])

def save_log(new_entry):
    df = load_logs()
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(LOG_FILE, index=False)

def main():
    st.title("Instrument Maintenance Calendar")

    instrument = st.selectbox("Select Instrument", ["GC-001", "GC-002", "GC-003"])
    with st.form("log_maintenance"):
        date = st.date_input("Date", value=datetime.today())
        action = st.text_input("Action Performed")
        tech = st.text_input("Performed By")
        notes = st.text_area("Notes")
        submitted = st.form_submit_button("Log Maintenance")

        if submitted:
            entry = {
                "Date": pd.to_datetime(date),
                "Instrument": instrument,
                "Action": action,
                "By": tech,
                "Notes": notes
            }
            save_log(entry)
            st.success("Maintenance logged successfully.")

    df = load_logs()
    st.subheader("Maintenance History")
    st.dataframe(df.sort_values("Date", ascending=False))

    if not df.empty:
        st.subheader("Maintenance Calendar")
        fig = px.scatter(df, x="Date", y="Instrument", color="Action", hover_data=["By", "Notes"], height=400)
        st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
