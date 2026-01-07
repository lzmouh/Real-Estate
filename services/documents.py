import os
from config import UPLOAD_PATH

def save_document(flat, file):
    path = os.path.join(UPLOAD_PATH, flat)
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, file.name), "wb") as f:
        f.write(file.getbuffer())
