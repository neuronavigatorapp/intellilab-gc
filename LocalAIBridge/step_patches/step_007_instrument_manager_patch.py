def build():
    path = "app/pages/instrument_dashboard.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# TODO: Implement Streamlit page: instrument_dashboard.py\n")
    return [path]
