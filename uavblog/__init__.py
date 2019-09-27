#where we initiualize our application and bring together different components and also tells python that this is a package
#we get to import all the external modules at this point and create the necessary instances
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

#the secret key helps also stop the modification of the secure cookies that we created in the remember me for login credentials
app.config["SECRET_KEY"]="fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)#handles all the user sessions in the background thus works in the models.py
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

#mind the positioning of the importation so as to avoid circular importation
from uavblog import routes