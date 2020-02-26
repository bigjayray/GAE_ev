import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from myuser import MyUser
from ev import EV

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)


class Details(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        name = self.request.get('name')
        manufacturer = self.request.get('manufacturer')
        year = int(self.request.get('year'))

        query = EV.query(ndb.AND(EV.manufacturer == manufacturer, EV.name == name, EV.year == year))

        template_values = {
            'user': user,
            'query' : query
        }

        template = JINJA_ENVIRONMENT.get_template('details.html')
        self.response.write(template.render(template_values))
