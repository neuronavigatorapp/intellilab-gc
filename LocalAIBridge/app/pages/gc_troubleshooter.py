import streamlit as st

def mock_ai_response(prompt):
    if "tailing" in prompt.lower():
        return "Tailing may be caused by active sites in the liner or column. Try changing the liner or trimming the column."
    elif "no peaks" in prompt.lower():
        return "Check the injection, signal cable, and whether the inlet is still in splitless hold."
    else:
        return "Check gas flow, column installation, detector connectivity, and oven timing."

def main():
    st.title("GC AI Troubleshooter")

    if "history" not in st.session_state:
        st.session_state.history = []

    prompt = st.text_input("Describe the GC issue you're facing:")
    if prompt:
        response = mock_ai_response(prompt)
        st.session_state.history.append((prompt, response))

    if st.session_state.history:
        st.subheader("Troubleshooting History")
        for i, (q, r) in enumerate(reversed(st.session_state.history), 1):
            st.markdown(f"**{i}.** 🤔 *{q}*  
🧠 {r}")

if __name__ == "__main__":
    main()
