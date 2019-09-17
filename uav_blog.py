from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY']='fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e'

posts = [
  {
   'author':'Dr. Mary',
   'title':'UAV Design1',
   'content':'First class to do this course work',
   'date_posted':'2019-12-13'
  },
  {
    'author':'Professor Sameer',
    'title':'UAV Design2',
    'content':'First class to do this course work',
    'date_posted':'2019-12-14'
  }
]

@app.route('/')
@app.route('/home')
def home():
	return render_template ('home.html',posts = posts)

@app.route('/about')
def about():
	return render_template('about.html',title = 'About')

@app.route('/register')
def register():
	form = RegistrationForm()#creating an instance of the registration form
	return render_template('register.html',title = 'Register',form = form)

@app.route('/login')
def login():
	form = LoginForm()#creating an instance of the login form
	return render_template('login.html',title = 'Login',form = form)


if __name__ == '__main__':
	app.run(debug = True)