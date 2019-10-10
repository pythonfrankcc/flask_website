'''initializinng of the project as a package and also ties together what we need for our app'''
#we get to import all the external modules at this point and create the necessary instances
from flask import Flask
#import os-since its unused
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt#this is a hashing module that prevents people from acquiring the login credentials in plain text even if the database is compromised
from flask_login import LoginManager#is used to manage user sessions in the background
from flask_mail import Mail
from uavblog.config import Config#importing the Config class in the config.py
#remember that anytime python imports sth from a module it still gets to run the entire module

#creating a database instance
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()#handles all the user sessions in the background thus works in the models.py
login_manager.login_view = 'users.login'#this is similar to what we would save in the url_for account this tells the login extension where to get the login page
login_manager.login_message_category = 'info'#changes the category of the flash messages with a  bootstrap class 'info'

#initialization of the extension
 
mail = Mail()
#mind the positioning of the importation so as to avoid circular importation since the routes are making the importation of the app
def create_app(config_class=Config):
	#the arguement is what configuration object you want to use
    app = Flask(__name__)
    app.config.from_object(Config)
    #the four extensions used
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
	from uavblog.users.routes import users
	from uavblog.posts.routes import posts
	from uavblog.main.routes import main
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(main)

    return app