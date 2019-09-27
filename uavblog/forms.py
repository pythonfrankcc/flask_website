'''the database structure of the site'''
#remember on importation of a module python runs the whole module
from flask_wtf import FlaskForm#uses this instead of the html creation of the forms
from flask_login import current_user
from wtforms import StringField#enables us to create strings for usernames and other string fields
from wtforms import PasswordField,SubmitField,BooleanField
from wtforms.validators import DataRequired, Length ,Email,EqualTo, ValidationError
from uavblog.models import User

class RegistrationForm(FlaskForm):
	tutor_username = StringField('Tutor Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
                        validators=[DataRequired(), Email()])
	password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=10)])
	password_confirmation =PasswordField('Password Confirmation',
                                     validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField("Sign Up now")




	def validate_username(self,username):
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('That username is already taken.Please choose a different one.')

	def validate_email(self,email):
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('That email already exists')


#now lets create a login form
class LoginForm(FlaskForm):
	email = StringField("Email",validators =[DataRequired(),Email])#want the users to login using the email instead of username
	password = PasswordField("Password",validators=[DataRequired(),Length(min=6,max=10)])
	#password_confirmation = Password("Password Confirmation",validators = [DataRequired(),EqualTo("password")]) no longer required as they confirmed the password during registration
	remember = BooleanField("Remember Me")#allows users to stayed login for sometime after the browser closes using secure cookie
	submit = SubmitField("Login")


#now lets create a login form
class UpdateAccountForm(FlaskForm):
	tutor_username = StringField('Tutor Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
                        validators=[DataRequired(), Email()])
	submit = SubmitField("Update")




	def validate_username(self,username):
		if username.data != current_user. username:
			user = User.query.filter_by(username = username.data).first()
			if user:
				raise ValidationError('That username is already takem.Please choose a different one.')

	def validate_email(self,email):
		if username.data != current_user. username:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('That email already exists')
