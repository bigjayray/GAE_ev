import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from addev import AddEv
from ev import EV
from details import Details

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()


        template_values = {
            'user': user
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Search':
            name = self.request.get('ev_name')
            manufacturer = self.request.get('ev_manufacturer')
            year = int(self.request.get('ev_year') or 0)
            battery_size = float(self.request.get('ev_battery_size') or 0)
            WLTP_range = float(self.request.get('ev_WLTP_Range') or 0)
            cost = float(self.request.get('ev_cost') or 0)
            power = float(self.request.get('ev_power') or 0)

            q = EV.query()

            if name:
                q = q.filter(EV.name == name)
            if manufacturer:
                q = q.filter(EV.manufacturer == manufacturer)
            if year:
                q = q.filter(EV.year == year)
            if battery_size:
                q = q.filter(EV.battery_size == battery_size)
            if WLTP_range:
                q = q.filter(EV.WLTP_range == WLTP_range)
            if cost:
                q = q.filter(EV.cost == cost)
            if power:
                q = q.filter(EV.power == power)

            q.fetch()

            template_values = {
                'q' : q
            }

            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
            
        elif action == 'Cancel':
            self.redirect('/')
