from flask import Flask, render_template, url_for, flash, redirect
from datetime import datetime
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SECRET_KEY"]="fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tutor_username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.tutor_username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    tutor_user_id = db.Column(db.Integer, db.ForeignKey('tutor_user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"

posts = [
  {
   "author":"Dr. Mary",
   "title":"UAV Design1",
   "content":"First class to do this course work",
   "date_posted":"2019-12-13"
  },
  {
    "author":"Professor Sameer",
    "title":"UAV Design2",
    "content":"First class to do this course work",
    "date_posted":"2019-12-14"
  }
]

@app.route("/")
@app.route("/home")
def home():
	return render_template ("home.html",posts = posts)

@app.route("/about")
def about():
	return render_template("about.html",title = "About")

#remember to make the page to be able to accept other methods in the page
@app.route("/register", methods=["GET", "POST"])
def register():
	form = RegistrationForm()#creating an instance of the registration form
	if form.validate_on_submit():
		flash(f"Account for {form.tutor_username.data} has been created!", "success")#this is the creation of a flash message
		return redirect(url_for("home"))#this redirects one back to the homepage on registration
	return render_template("register.html", title="Register", form=form)

@app.route("/login",methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check tutor_username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
	app.run(debug = True)