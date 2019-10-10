'''initializinng of the project as a package and also ties together what we need for our app'''
#we get to import all the external modules at this point and create the necessary instances
from flask import Flask
import os
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt#this is a hashing module that prevents people from acquiring the login credentials in plain text even if the database is compromised
from flask_login import LoginManager#is used to manage user sessions in the background
from flask_mail import Mail
#remember that anytime python imports sth from a module it still gets to run the entire module

app = Flask(__name__)

#the secret key helps also stop the modification of the secure cookies that we created in the remember me for login credentials
app.config["SECRET_KEY"]="fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"

#setting the sqlite database location and since its also the easiest to setup  which you define a relative path from the current file path you are in with 3 ///
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
#creating a database instance
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)#handles all the user sessions in the background thus works in the models.py
login_manager.login_view = 'login'#this is similar to what we would save in the url_for account this tells the login extension where to get the login page
login_manager.login_message_category = 'info'#changes the category of the flash messages with a  bootstrap class 'info'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True #the transport layer Security protocol is used as an alternative to ssh

#this is using the environment variables to hide sensitive information
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
#initialization of the extension
 
mail = Mail(app)
#mind the positioning of the importation so as to avoid circular importation since the routes are making the importation of the app
from uavblog import routes