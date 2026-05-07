import secrets
import os
from flask import current_app,url_for
from flaskblog import mail
from PIL import Image
from flask_mail import Message


def save_image(form_picture):
    random_hex=secrets.token_hex(8)
    _,f_ext=os.path.splitext(form_picture.filename)
    picture_fn=random_hex+f_ext
    picture_path=os.path.join(current_app.root_path,"static/profile_pic",picture_fn)
    
    i=Image.open(form_picture)
    i.thumbnail((125,125))
    i.save(picture_path)
    return picture_fn


def send_reset_mail(user):
    token=user.get_reset_token()
    msg=Message("password_reset_mail",sender=current_app.config['MAIL_DEFAULT_SENDER'],recipients=[user.email])
    link=url_for('users.reset_token', token=token, _external=True)
    msg.body=f'''if you want to reset the password click the link below:
{link}
    if you don't simply ignore this mail
''' 
    mail.send(msg)
