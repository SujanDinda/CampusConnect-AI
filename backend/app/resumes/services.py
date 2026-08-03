import os
import uuid

from werkzeug.utils import secure_filename
from flask import current_app

from app.extensions import db
from app.models.resume import Resume


def save_resume(file, user_id):

    upload_folder = os.path.join(
        current_app.root_path,
        "..",
        "uploads",
        "resumes"
    )

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    extension = file.filename.rsplit(".", 1)[1].lower()

    filename = (
        f"{user_id}_{uuid.uuid4().hex}.{extension}"
    )

    filename = secure_filename(filename)

    file_path = os.path.join(
        upload_folder,
        filename
    )

    file.save(file_path)

    resume = Resume(
        user_id=user_id,
        file_name=filename,
        file_path=file_path,
        file_size=os.path.getsize(file_path),
        mime_type=file.mimetype
    )

    db.session.add(resume)
    db.session.commit()

    return resume