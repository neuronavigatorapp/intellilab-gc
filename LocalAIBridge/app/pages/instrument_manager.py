import streamlit as st
from app.models import SessionLocal, Instrument, init_db
from sqlalchemy.exc import IntegrityError

def get_instruments():
    session = SessionLocal()
    instruments = session.query(Instrument).all()
    session.close()
    return instruments

def save_instrument(name, model, serial, location, status):
    session = SessionLocal()
    instrument = Instrument(
        name=name,
        model=model,
        serial=serial,
        location=location,
        status=status
    )
    session.add(instrument)
    try:
        session.commit()
        return True
    except IntegrityError:
        session.rollback()
        return False
    finally:
        session.close()

def main():
    st.title("Instrument Manager")

    with st.form("instrument_form"):
        name = st.text_input("Name")
        model = st.text_input("Model")
        serial = st.text_input("Serial Number")
        location = st.text_input("Location")
        status = st.selectbox("Status", ["Active", "Maintenance", "Offline"])
        submitted = st.form_submit_button("Add Instrument")

        if submitted:
            success = save_instrument(name, model, serial, location, status)
            if success:
                st.success("Instrument added successfully!")
                st.experimental_rerun()
            else:
                st.error("Failed to add instrument. Check for duplicate serial.")

    instruments = get_instruments()
    if instruments:
        st.subheader("Registered Instruments")
        for i in instruments:
            st.markdown(f"- **{i.name}** ({i.model}) — {i.status} @ {i.location}")

if __name__ == "__main__":
    init_db()
    main()
