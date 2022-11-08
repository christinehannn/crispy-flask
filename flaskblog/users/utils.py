import os
import secrets

from PIL import Image
from flask import url_for

from flaskblog import app
from flaskblog.utils import send_mailgun_email


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        app.root_path,
        'static/profile_pics',
        picture_fn
    )

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    body = (
        f'To reset your password, visit the following link: '
        f'{url_for("reset_token", token=token, _external=True)}\n'
        'If you did not make this request then simply ignore this email and '
        'no changes will be made.'
    )
    send_mailgun_email(
        user.email,
        'Password Reset Request',
        body
    )
