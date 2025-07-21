def build():
    path = "app/pages/column_inventory.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# TODO: Implement Streamlit page: column_inventory.py\n")
    return [path]
