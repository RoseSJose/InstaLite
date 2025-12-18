import os
from werkzeug.utils import secure_filename

def save_image(image, upload_folder):
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    filename = secure_filename(image.filename)
    path = os.path.join(upload_folder, filename)
    image.save(path)
    return f"/static/uploads/{filename}"