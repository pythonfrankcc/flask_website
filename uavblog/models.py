'''this represents the tables in our databases'''
#this are the list of  all the dependencies that the model uses 
from datetime import datetime
from uavblog import db,login_manager
from flask_login import UserMixin
#remember that anytime python imports a module it runs the entire module 


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model):
    '''creates the User relational table'''
    id = db.Column(db.Integer, primary_key=True)
    tutor_username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)#lazy enables us to load the data from the database in a single go for sqlalchemy
    #the posts in thhis model is not a column but is only used to show the relationship with the Post model while the backref allows us to get the user who created the Post

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
#__scr__ or __rpr_ shows how you want the user to look like when you print   


class Post(db.Model):
    '''creates the Post relational table'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    #this is to specify the user in the Post model we add the user id for the author  

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

#in the datetime function that you use to define the default datetime is not going to be called on date_posted account since we want to use the function time as the arguement