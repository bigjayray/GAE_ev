# imports
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

# Details class
class Details(webapp2.RequestHandler):

    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # gets id passed in the url
        id = self.request.get('id')

        # generates key
        key = ndb.Key('EV', int(id))

        # gets ev
        ev = key.get()

        # values to be rendered to the details.html page
        template_values = {
            'user': user,
            'ev' : ev
        }

        template = JINJA_ENVIRONMENT.get_template('details.html')
        self.response.write(template.render(template_values))

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'Edit':

            # generates ev
            id = self.request.get('id')
            key = ndb.Key('EV', int(id))
            ev = key.get()

            # assigns form values to the ev
            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))

            # adds ev to datastore
            ev.put()

            # redirects back to home page
            self.redirect('/')

        elif action == 'Delete':
            id = self.request.get('id')
            key = ndb.Key('EV', int(id))
            ev = key.get()

            # deletes ev
            ev.key.delete()
            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
