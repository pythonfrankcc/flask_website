'''importing the relevant dependencies'''
from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from uavblog import db
from uavblog.models import Post
from uavblog.posts.forms import PostForm


#creating an instance of the blueprint just like for the flask app
posts = Blueprint('posts', __name__)


#the instance of the route is now specific to this post
@posts.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)#adding a post to a database
        db.session.commit()
        flash('Your post has been created!', 'success')#category of success
        return redirect(url_for('main.home'))
    return render_template('create_post.html', title='New Post',
                           form=form, legend='New Post')    

@posts.route("/post/<int:post_id>")#this is allowed in flask to allow us to query a route by the id 
def post(post_id):
    post = Post.query.get_or_404(post_id)#fetching the post and since we are getting sth by the id we can use the get command
    return render_template('post.html', title=post.title, post=post)

@posts.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        return redirect(url_for('posts.post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post',
                           form=form, legend='Update Post')

@posts.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('main.home'))

#this route is used to display the posts that are associated with a specific user