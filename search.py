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

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

# Search Class
class Search(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # values to be rendered to the search.html page
        template_values = {
            'user': user
        }

        template = JINJA_ENVIRONMENT.get_template('search.html')
        self.response.write(template.render(template_values))

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'Search':
            name = self.request.get('ev_name')
            manufacturer = self.request.get('ev_manufacturer')
            year_upper = self.request.get('ev_year_upper')
            year_lower = self.request.get('ev_year_lower')
            battery_size_upper = self.request.get('ev_battery_size_upper')
            battery_size_lower = self.request.get('ev_battery_size_lower')
            WLTP_range_upper = self.request.get('ev_WLTP_Range_upper')
            WLTP_range_lower = self.request.get('ev_WLTP_Range_lower')
            cost_upper = self.request.get('ev_cost_upper')
            cost_lower = self.request.get('ev_cost_lower')
            power_upper = self.request.get('ev_power_upper')
            power_lower = self.request.get('ev_power_lower')

            # querys ev
            query1 = EV.query().fetch(keys_only=True)
            query = EV.query().fetch(keys_only=True)

            # selection statement values from form
            if name:
                query2 = EV.query(EV.name == name).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if manufacturer:
                query2 = EV.query(EV.manufacturer == manufacturer).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if year_upper:
                query2 = EV.query(EV.year <= int(year_upper)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if year_lower:
                query2 = EV.query(EV.year >= int(year_lower)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if battery_size_upper:
                query2 = EV.query(EV.battery_size <= float(battery_size_upper)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if battery_size_lower:
                query2 = EV.query(EV.battery_size >= float(battery_size_lower)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if WLTP_range_upper:
                query2 = EV.query(EV.WLTP_range <= float(WLTP_range_upper)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if WLTP_range_lower:
                query2 = EV.query(EV.WLTP_range >=  float(WLTP_range_lower)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if cost_upper:
                query2 = EV.query(EV.cost <= float(cost_upper)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if cost_lower:
                query2 = EV.query(EV.cost >= float(cost_lower)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if power_upper:
                query2 = EV.query(EV.power <= float(power_upper)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))
            if power_lower:
                query2 = EV.query(EV.power >= float(power_lower)).fetch(keys_only=True)
                query1 = (set(query1).intersection(query2))


            # query returns a list containing entity objects
            total_query = ndb.get_multi(set(query).intersection(query1))

            # values to be rendered to the search.html page
            template_values = {
                'user': user,
                'total_query' : total_query
            }

            template = JINJA_ENVIRONMENT.get_template('search.html')
            self.response.write(template.render(template_values))
        elif action == 'Cancel':
            self.redirect('/')
