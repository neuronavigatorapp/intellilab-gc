def build():
    from pathlib import Path
    import textwrap

    upload_path = Path("utils/instrument_images.py")
    upload_path.parent.mkdir(parents=True, exist_ok=True)

    upload_path.write_text(textwrap.dedent("""
        import shutil
        from pathlib import Path

        def get_image_path(instrument_id):
            return Path("data/images") / f"{instrument_id}.png"

        def save_uploaded_image(uploaded_file, instrument_id):
            dest = get_image_path(instrument_id)
            dest.parent.mkdir(parents=True, exist_ok=True)
            with open(dest, "wb") as f:
                shutil.copyfileobj(uploaded_file, f)

        def image_exists(instrument_id):
            return get_image_path(instrument_id).exists()
    """))

    print("Patch 024 applied: Instrument image upload support added.")
    return [], [], []

if __name__ == "__main__":
    build()
