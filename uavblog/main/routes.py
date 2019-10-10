'''importing the relevant dependencies'''
from flask import render_template, request, Blueprint
from uavblog.models import Post



#creating an instance of the blueprint just like for the flask app
main = Blueprint('main', __name__)

@main.route("/")#decorators using the init in the uavblog
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)#page is an optional parameter in the url,default page is set to one and the int dictates that if a person wants a page no thyen it must be equal to an interger
    #posts = Post.query.all()#grabbing all the post from the database
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page,per_page=5)#this allows you to specify the no of posts you want to display per page and this enhances the speed of your page and is a flask sqlalchemy module
    #the order_by in the post alows you to be able to arrange the posts allowing the latest post to be at the top
    return render_template ("home.html")

@main.route("/about")
def about():
	return render_template("about.html",title = "About")



