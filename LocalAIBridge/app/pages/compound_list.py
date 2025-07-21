import streamlit as st
from app.models import SessionLocal, Compound

def get_all_compounds():
    session = SessionLocal()
    compounds = session.query(Compound).all()
    session.close()
    return compounds

def update_compound(compound_id, updated_data):
    session = SessionLocal()
    compound = session.query(Compound).get(compound_id)
    for key, value in updated_data.items():
        setattr(compound, key, value)
    session.commit()
    session.close()

def delete_compound(compound_id):
    session = SessionLocal()
    compound = session.query(Compound).get(compound_id)
    session.delete(compound)
    session.commit()
    session.close()

def compound_table():
    st.title("Compound List")

    compounds = get_all_compounds()

    if not compounds:
        st.info("No compounds found.")
        return

    for compound in compounds:
        with st.expander(f"{compound.name} ({compound.formula})"):
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"Edit {compound.id}"):
                    with st.form(f"edit_form_{compound.id}"):
                        name = st.text_input("Name", compound.name)
                        formula = st.text_input("Formula", compound.formula)
                        mw = st.number_input("Molecular Weight", value=compound.molecular_weight)
                        method_tag = st.text_input("Method Tag", compound.method_tag)
                        rt = st.number_input("Retention Time", value=compound.retention_time)
                        bp = st.number_input("Boiling Point", value=compound.boiling_point)
                        submitted = st.form_submit_button("Save Changes")
                        if submitted:
                            update_compound(compound.id, {
                                "name": name,
                                "formula": formula,
                                "molecular_weight": mw,
                                "method_tag": method_tag,
                                "retention_time": rt,
                                "boiling_point": bp
                            })
                            st.success("Compound updated successfully.")
                            st.experimental_rerun()

            with col2:
                if st.button(f"Delete {compound.id}"):
                    confirm = st.radio(f"Are you sure you want to delete {compound.name}?", ["No", "Yes"], index=0, key=f"del_{compound.id}")
                    if confirm == "Yes":
                        delete_compound(compound.id)
                        st.warning(f"{compound.name} has been deleted.")
                        st.experimental_rerun()

def main():
    compound_table()

if __name__ == "__main__":
    main()
