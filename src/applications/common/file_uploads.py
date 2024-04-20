import hashlib
import pathlib
from time import time

from django.db import models


def upload_to(prefix: str, instance: models.Model, filename: str) -> pathlib.Path:
    _, extension = pathlib.Path(filename).stem, pathlib.Path(filename).suffix
    vector = int(time())
    sha_filename = hashlib.sha3_256(
        bytes(f'{vector}:{filename}'.encode())
    ).hexdigest()
    path = pathlib.Path(
        'avatars',
        sha_filename[-2:],
        sha_filename[-5:-2],
        sha_filename + extension
    )
    return path