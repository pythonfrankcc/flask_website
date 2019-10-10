''''importing the relevant dependencies'''
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
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




	def validate_username(self,tutor_username):
			user = User.query.filter_by(tutor_username = tutor_username.data).first()
			if user:
				raise ValidationError('That Tutor Username is already taken.Please choose a different one.')

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


#now lets create a update form
class UpdateAccountForm(FlaskForm):
	tutor_username = StringField('Tutor Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email',
                        validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture',validators=[FileAllowed(['png','jpg'])])

	submit = SubmitField("Update")




	def validate_username(self,tutor_username):
		if tutor_username.data != current_user.tutor_username:
			user = User.query.filter_by(tutor_username = tutor_username.data).first()
			if user:
				raise ValidationError('That username is already taken.Please choose a different one.')

	def validate_email(self,email):
		if tutor_username.data != current_user.tutor_username:
			user = User.query.filter_by(email = email.data).first()
			if user:
				raise ValidationError('That email already exists')


''''creating a requestreset form for the users to be able to change their login credentials'''
class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
