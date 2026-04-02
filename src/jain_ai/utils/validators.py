import os

from ..constants.settings import ALLOWED_EXTENSIONS


def allowed_file(filename):
    extension = os.path.splitext(filename.lower())[1]
    return extension in ALLOWED_EXTENSIONS
