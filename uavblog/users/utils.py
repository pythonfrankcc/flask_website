'''importing the relevant dependencies'''
import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from uavblog import mail
#from uavblog import mail,app-we are going to remove the app since we created a function that acts as a blueprint for the app creation


'''saving the profile picture by a user'''
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)#randomizing the name of the image so as not to collide with what we already have in the databasae acting as the base of our file name
    _, f_ext = os.path.splitext(form_picture.filename)#the underscore allows us to throw away the variable name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/procfile_pics', picture_fn)#joining all the paths together
    #resizing the image before upload to minimise the amount of space taken up by the picture and also speed up the website
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    form_picture.save(picture_path)


    return picture_fn

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('users.reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
#remember when passing a variable to an f'string we only use a single curly braces unlike 2 curly braces that we are used to seeing in the jinja 2 templates
#_external = True is used in order to get an absolute url rather than a relative url(this are used within the locality of our application ) but absolute like the one we want we want to have the full domain since its email but if your message is  complicated enough you will need to use the jinja templates to create the message

