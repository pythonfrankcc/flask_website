from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"]="fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"

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
		flash(f"Account for {form.username.data} has been created!", "success")#this is the creation of a flash message
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
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)


if __name__ == "__main__":
	app.run(debug = True)