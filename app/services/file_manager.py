from pathlib import Path


UPLOAD_FOLDER = Path("data/uploads")


def create_upload_folder():
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


def save_uploaded_file(uploaded_file):
    create_upload_folder()

    file_path = UPLOAD_FOLDER / uploaded_file.name

    with open(file_path, "wb") as file:
        file.write(uploaded_file.getbuffer())

    return file_path