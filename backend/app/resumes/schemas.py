ALLOWED_EXTENSIONS = {
    "pdf",
    "docx"
}

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB


def allowed_file(filename):

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in ALLOWED_EXTENSIONS