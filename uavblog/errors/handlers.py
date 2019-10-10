from flask import Blueprint,render_template

errors = Blueprint('errors',__name__)

#we use the method called app_errorhandler instead of errorhandler cz it works for the entire application instead of just the above blueprint and that is what we want in our case

#use a decorator just as the route decorators
#used when the site is not reachable or the user has entered a wrong location on the web
@errors.app_errorhandler(404)
def error_404(error):
    return render_template('errors/404.html'), 404#the 404 at the end is the status code that is allowed in flask with the default value being 200

'''error for an unallowed activity,example, another user trying to change a post that they didn't post'''
@errors.app_errorhandler(403)
def error_403(error):
    return render_template('errors/403.html'), 403

'''general error for an unreachable server function'''
@errors.app_errorhandler(500)
def error_500(error):
    return render_template('errors/500.html'), 500