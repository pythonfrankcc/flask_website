#where we initiualize our application and bring together different components and also tells python that this is a package
from flask import Flask
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"]="fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

#mind the positioning of the importation so as to avoid circular importation
from uav_blog import routes