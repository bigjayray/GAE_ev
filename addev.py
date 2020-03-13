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


class AddEv(webapp2.RequestHandler):

    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        if user:
            template_values = {
                'user': user
            }

            template = JINJA_ENVIRONMENT.get_template('addev.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        action = self.request.get('button')

        ev = EV()

        if action == 'Add':

            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_Range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))

            query = EV.query(ndb.AND(EV.manufacturer == ev.manufacturer, EV.name == ev.name, EV.year == ev.year))

            if query.count() > 0:
                error = 'Error: EV already exists!'
                template_values = {
                    'error' : error,
                    'user': user
                }

                template = JINJA_ENVIRONMENT.get_template('addev.html')
                self.response.write(template.render(template_values))
                return
                # error = 'EV already entered into datastore'
                self.redirect('/addev')
            else:
                ev.put()
                self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
