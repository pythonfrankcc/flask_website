'''route decorators to the various pages'''
import secrets#allows you to create a bunch of random names as the extension file for naming
import os#allows you to upload file as the extension that they uploades
from PIL import Image
from flask import render_template, url_for, flash, redirect,request,abort
from uavblog import app, db, bcrypt,mail
from uavblog.forms import RegistrationForm, LoginForm, UpdateAccountForm,PostForm, RequestResetForm, ResetPasswordForm
#from flaskblog.forms import (RegistrationForm, LoginForm, UpdateAccountForm,PostForm, RequestResetForm, ResetPasswordForm)#alternatively if your imports get too many you can do this which is putting all your imports in a bracket
from datetime import datetime
from uavblog.models import User, Post
from flask_login import login_user,current_user, logout_user, login_required
#the login_required module ensures that you cannot view the account page until you have been logged in 
from flask_mail import Message


@app.route("/")#decorators using the init in the uavblog
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)#page is an optional parameter in the url,default page is set to one and the int dictates that if a person wants a page no thyen it must be equal to an interger
    #posts = Post.query.all()#grabbing all the post from the database
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page=5)#this allows you to specify the no of posts you want to display per page and this enhances the speed of your page and is a flask sqlalchemy module
    #the order_by in the post alows you to be able to arrange the posts allowing the latest post to be at the top
    return render_template ("home.html")

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')#this is a situation when you weant it to be a string rather than a byte
        user = User(tutor_username=form.tutor_username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your Account has been created !You can now log in!","success")#this is the creation of a flash message with the second parameter in the message allowing you to have a category
        return redirect(url_for('login'))#this redirects one back to the homepage on registration with this being the function that is the home page
    return render_template('register.html', title='Register', form=form)



@app.route("/login",methods=["GET", "POST"])
#this allows the page to accept the post request that you send to it by filling data in the various fields
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data) 
            next_page = request.args.get('next')#args is a dictionary but avoid accessing next using the square brackets and key name as that would throw an error if the key name doesnt exist so just use the get method
            return redirect(next_page) if next_page else redirect(url_for('home'))#this is a ternary conditional in python
            #the part above just makes sure that if there is a next query on the url on page we can acquire it to directly take the user to the next page without having to take the user to another page and basically improves user experience 
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template("login.html", title="Login", form=form)
#if parameters dont match it returns one to the login page again

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


'''saving the profile picture by a user'''
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)#randomizing the name of the image so as not to collide with what we already have in the databasae acting as the base of our file name
    _, f_ext = os.path.splitext(form_picture.filename)#the underscore allows us to throw away the variable name
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/procfile_pics', picture_fn)#joining all the paths together
    #resizing the image before upload to minimise the amount of space taken up by the picture and also speed up the website
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    form_picture.save(picture_path)


    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
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
    return redirect(url_for('account'))
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

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)#adding a post to a database
        db.session.commit()
        flash('Your post has been created!', 'success')#category of success
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')    

@app.route("/post/<int:post_id>")#this is allowed in flask to allow us to query a route by the id 
def post(post_id):
    post = Post.query.get_or_404(post_id)#fetching the post and since we are getting sth by the id we can use the get command
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
#you have to be logged in to be able to update
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)#this is a http response of a forbidden route
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        #since we are updating sth that is alraedy in the database we do not need to add we just commit
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))

#this route is used to display the posts that are associated with a specific user

@app.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(tutor_username=username).first_or_404()#the parameter username is from the route that we get from the route function
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('user_posts.html', posts=posts, user=user)#create a user_posts.html that handles all the posts for a specific user
#a backslash allows you to break a line into multiple lines

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)
#remember when passing a variable to an f'string we only use a single curly braces unlike 2 curly braces that we are used to seeing in the jinja 2 templates
#_external = True is used in order to get an absolute url rather than a relative url(this are used within the locality of our application ) but absolute like the one we want we want to have the full domain since its email but if your message is  complicated enough you will need to use the jinja templates to create the message


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password', form=form)

@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)#inheritance from the model page
    if user is None:
        flash('That is an invalid or expired token', 'warning')#the tag on the message is a yellow one 
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password', form=form)