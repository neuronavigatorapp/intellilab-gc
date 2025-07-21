import streamlit as st
from app.models import SessionLocal, Compound

def main():
    st.title("Compound Entry Form")

    with st.form("compound_form"):
        name = st.text_input("Compound Name")
        formula = st.text_input("Formula")
        mw = st.number_input("Molecular Weight", step=0.01)
        method_tag = st.text_input("Method Tag")
        rt = st.number_input("Retention Time (min)", step=0.01)
        bp = st.number_input("Boiling Point (°C)", step=0.01)
        submitted = st.form_submit_button("Submit")

        if submitted:
            session = SessionLocal()
            compound = Compound(
                name=name,
                formula=formula,
                molecular_weight=mw,
                method_tag=method_tag,
                retention_time=rt,
                boiling_point=bp
            )
            session.add(compound)
            session.commit()
            session.close()
            st.success("Compound saved successfully!")

if __name__ == "__main__":
    main()
