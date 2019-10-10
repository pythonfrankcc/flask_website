import os




class Config:
	#the secret key helps also stop the modification of the secure cookies that we created in the remember me for login credentials
	SECRET_KEY = "fc29601ad9a75c5a35e421fd9d546aa4ec3ef1052e"
	#setting the sqlite database location and since its also the easiest to setup  which you define a relative path from the current file path you are in with 3 ///
	SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'#when using sqlite there is nothing sensitive in the database uri but with postgress the username and password are going to be in the connection string 
	#look at the windows video for making the database uri and username a secret using the environment variables
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 587
	MAIL_USE_TLS = True #the transport layer Security protocol is used as an alternative to ssh
	#this is using the environment variables to hide sensitive information
	MAIL_USERNAME = os.environ.get('EMAIL_USER')
	MAIL_PASSWORD = os.environ.get('EMAIL_PASS')