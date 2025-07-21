import streamlit as st
import pandas as pd
import plotly.express as px

def flag_peaks(df):
    df["Flag"] = ""
    flagged = 0
    for i, row in df.iterrows():
        flags = []
        if row["Retention Time"] < 0.5:
            flags.append("Early Elution")
        if row["Area"] < 500:
            flags.append("Low Area")
        if row["Width"]/max(row["Retention Time"], 0.1) > 0.25:
            flags.append("Tailing")
        if flags:
            df.at[i, "Flag"] = ", ".join(flags)
            flagged += 1
    return df, flagged

def main():
    st.title("GC CSV Analyzer")

    uploaded = st.file_uploader("Upload CSV file", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.subheader("Raw Data")
        st.dataframe(df)

        if {"Retention Time", "Area", "Width"}.issubset(df.columns):
            df, flagged_count = flag_peaks(df)

            st.subheader("Peak Analysis")
            fig = px.scatter(df, x="Retention Time", y="Area", color="Flag",
                             title="Retention Time vs Area", height=400)
            st.plotly_chart(fig, use_container_width=True)

            if flagged_count:
                st.warning(f"{flagged_count} peaks flagged for review.")
                if st.checkbox("Show flagged only"):
                    st.dataframe(df[df["Flag"] != ""])
            else:
                st.success("No issues found in this dataset.")
        else:
            st.error("CSV must include: Retention Time, Area, and Width columns.")

if __name__ == "__main__":
    main()
