def update_dashboard_widgets():
    path = "app/pages/instrument_dashboard.py"
import os

def update_dashboard_widgets():
    path = "app/pages/instrument_dashboard.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "a", encoding="utf-8") as f:
        f.write("""\n
# === Streamlit Enhancements ===
selected = st.selectbox("Filter by Instrument", ["All"] + INSTRUMENTS)

if selected != "All":
    df = df[df["Instrument"] == selected]

st.subheader("Method Assignment Breakdown")
method_counts = df["Assigned Method"].value_counts()
st.bar_chart(method_counts)

st.subheader("Status Distribution")
status_counts = df["Status"].value_counts()
st.bar_chart(status_counts)
""")
    return [path], [], []

def build():
    return update_dashboard_widgets()
