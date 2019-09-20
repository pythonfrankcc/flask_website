from flask import render_template, url_for, flash, redirect,request
from uavblog import app, db, bcrypt
from uavblog.forms import RegistrationForm, LoginForm
from datetime import datetime
from uavblog.models import User, Post
from flask_login import login_user,current_user, logout_user, login_required


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

@app.route("/")#decorators using the init in the uavblog
@app.route("/home")
def home():
	return render_template ("home.html",posts = posts)

@app.route("/about")
def about():
	return render_template("about.html",title = "About")

#remember to make the page to be able to accept other methods in the page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()#creating an instance of the registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! Thank you !You are now able to log in", "success")#this is the creation of a flash message
        return redirect(url_for('login'))#this redirects one back to the homepage on registration
    return render_template('register.html', title='Register', form=form)



@app.route("/login",methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')