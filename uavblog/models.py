'''this represents the tables in our databases'''
#this are the list of  all the dependencies that the model uses 
from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer#generating a secure time sensitive token
from uavblog import db,login_manager,app#we are importing app since we need the  app's secret key
from flask_login import UserMixin
#remember that anytime python imports a module it runs the entire module 

''''this reloads the user from the user id stored in the session'''
#the extension expects the user model to have atributes such as: is authenticated ,is active,is anonymous,get id but this is done for us by the UserMixin 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    '''creates the User relational table'''
    id = db.Column(db.Integer, primary_key=True)
    tutor_username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)#lazy enables us to load the data from the database in a single go for sqlalchemy
    #the posts in this model is not a column but is only used to show the relationship with the Post model while the backref allows us to get the user who created the Post and all their attributes
    '''creation of a token'''
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')
    #this tells python that this is a static method so it should not expect the self parameter passed
    '''validating the token created'''
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.tutor_username}', '{self.email}', '{self.image_file}')"
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