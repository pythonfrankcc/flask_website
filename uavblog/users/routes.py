'''importing the relevant dependencies'''
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from uavblog import db, bcrypt
from uavblog.models import User, Post
from uavblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from uavblog.users.utils import save_picture, send_reset_email


#creating an instance of the blueprint just like for the flask app
users = Blueprint('users', __name__)


#remember to make the page to be able to accept other methods in the page
#this allows the routes to be more specific to the user as the route
@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()#creating an instance of the registration form
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')#this is a situation when you weant it to be a string rather than a byte
        user = User(tutor_username=form.tutor_username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account has been created !You can now log in!","success")#this is the creation of a flash message with the second parameter in the message allowing you to have a category
        return redirect(url_for('users.login'))#this redirects one back to the homepage on registration with this being the function that is the home page
    return render_template('register.html', title='Register', form=form)



@users.route("/login",methods=["GET", "POST"])
#this allows the page to accept the post request that you send to it by filling data in the various fields
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) 
            next_page = request.args.get('next')#args is a dictionary but avoid accessing next using the square brackets and key name as that would throw an error if the key name doesnt exist so just use the get method
            return redirect(next_page) if next_page else redirect(url_for('main.home'))#this is a ternary conditional in python
            #the part above just makes sure that if there is a next query on the url on page we can acquire it to directly take the user to the next page without having to take the user to another page and basically improves user experience 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)
#if parameters dont match it returns one to the login page again

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
  form = UpdateAccountForm()
  if form.validate_on_submit():
    if form.picture.data:
      picture_file = save_picture(form.picture.data)
      current_user.image_file = picture_file
    current_user.tutor_username = form.tutor_username.data#made easier by using sql_Alchemy
    current_user.email = form.email.data
    db.session.commit()
    flash('Your account has been updated!', 'success')
    #getting an update on an account overwrites on the existent account
    return redirect(url_for('users.account'))
    #it is best that you do a redirect before you return a render as it results to no resubmission of posts method since a redirect sends out a get method instead of post
  elif request.method == 'GET':#this is used to populate the account in advance
    form.tutor_username.data = current_user.tutor_username
    form.email.data = current_user.email
    #this is the default path of the image_file
  image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
  #instead you could have used an f'string 
  return render_template('account.html', title='Account',
                           image_file=image_file, form=form)  
#this allows you to pass in the image file onto the accounts template as a variable image file

@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(tutor_username=username).first_or_404()#the parameter username is from the route that we get from the route function
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)#create a user_posts.html that handles all the posts for a specific user
#a backslash allows you to break a line into multiple lines

@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)#inheritance from the model page
    if user is None:
        flash('That is an invalid or expired token', 'warning')#the tag on the message is a yellow one 
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title='Reset Password', form=form)
