def build():
    path = "app/pages/maintenance_calendar.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# TODO: Implement Streamlit page: maintenance_calendar.py\n")
    return [path]
