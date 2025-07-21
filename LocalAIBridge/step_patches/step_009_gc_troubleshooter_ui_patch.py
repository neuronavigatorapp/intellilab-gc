def build():
    path = "app/pages/gc_troubleshooter.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# TODO: Implement Streamlit page: gc_troubleshooter.py\n")
    return [path]
