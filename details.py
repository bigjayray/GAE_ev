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

        id = self.request.get('id')

        key = ndb.Key('EV', int(id))
        ev = key.get()

        template_values = {
            'user': user,
            'ev' : ev
        }

        template = JINJA_ENVIRONMENT.get_template('details.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Edit':

            id = self.request.get('id')
            key = ndb.Key('EV', int(id))
            ev = key.get()

            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))

            ev.put()

            self.redirect('/')

        elif action == 'Delete':
            id = self.request.get('id')
            key = ndb.Key('EV', int(id))
            ev = key.get()
            
            ev.key.delete()

        elif action == 'Cancel':
            self.redirect('/')
