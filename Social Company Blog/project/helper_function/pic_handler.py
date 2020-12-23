import os
from PIL import Image
from flask import current_app, url_for


def add_picture(pic_upload, username):
    file_name = pic_upload.filename
    ext_type = file_name.split(".")[-1]
    storage_file = str(username) + ext_type
    file_path = os.path.join(current_app.root_path, "static\profile_pic", storage_file)
    pic = Image.open(pic_upload)
    pic.thumbnail((200, 200))
    pic.save(file_path)
    return storage_file
