from flask import render_template, url_for, flash, redirect
from uav_blog import app 
from uav_blog.forms import RegistrationForm, LoginForm
from datetime import datetime
from uav_blog.models import User, Post


posts = [
  {
   "author":"Dr. Mary",
   "title":"UAV Design1",
   "content":"First class to do this course work",
   "date_posted":datetime.utcnow().replace(second=0, microsecond=0)
  },
  {
    "author":"Professor Sameer",
    "title":"UAV Design2",
    "content":"First class to do this course work",
    "date_posted":datetime.utcnow().replace(second=0, microsecond=0)#this keeps updating to the current time and you do not want that
  }
]

@app.route("/")#decorators using the init in the uav_blog
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
