def build():
    path = "app/pages/method_preview.py"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write("# TODO: Implement Streamlit page: method_preview.py\n")
    return [path]
