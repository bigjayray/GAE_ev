# imports
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from addev import AddEv
from ev import EV
from details import Details
from search import Search
from compare import Compare
from reviews import Reviews

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# MainPage class
class MainPage(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = None

        # get current user
        user = users.get_current_user()

        # selection statement for user
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'

            myuser_key = ndb.Key('MyUser', user.user_id())
            myuser = myuser_key.get()

            if myuser == None:
                welcome = 'Welcome to the application'
                myuser = MyUser(id=user.user_id())
                myuser.put()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'

        # values to be rendered to the main.html page
        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))


# starts the web application and specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addev', AddEv),
    ('/details', Details),
    ('/search', Search),
    ('/compare', Compare),
    ('/reviews', Reviews),
], debug=True)
