import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from myuser import MyUser
from ev import EV

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Compare(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # query the datastore for ev
        q = EV.query()

        # values to be rendered to the compare.html page
        template_values = {
            'user': user,
            'q' : q
        }

        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # query the datastore for ev
        q = EV.query()
        error = ''

        # get value of button clicked
        action = self.request.get('button')

        # selection statement for button
        if action == 'Compare':

            # gets the ids of evs selected
            ev_ids = self.request.get_all('evs')
            if len(ev_ids) < 2:
                error = 'Error: Choose at least two evs'
                template_values = {
                    'error' : error,
                    'q' : q,
                    'user' : user
                }

                template = JINJA_ENVIRONMENT.get_template('compare.html')
                self.response.write(template.render(template_values))
                return
            # python list of evs
            EVs = []
            for id in ev_ids:
                key = ndb.Key('EV', int(id))
                ev = key.get()
                EVs.append(ev)

            max_battery_size = 0
            min_battery_size = 9223372036854775807
            max_WLTP_range = 0
            min_WLTP_range = 9223372036854775807
            max_cost = 0
            min_cost = 9223372036854775807
            max_power = 0
            min_power = 9223372036854775807
            max_rating = 0
            min_rating = 9223372036854775807

            # loop through the list of evs to find max and min values
            for ev in EVs:
                if max_battery_size < ev.battery_size:
                    max_battery_size = ev.battery_size
                if min_battery_size > ev.battery_size:
                    min_battery_size = ev.battery_size
                if max_WLTP_range < ev.WLTP_range:
                    max_WLTP_range = ev.WLTP_range
                if min_WLTP_range > ev.WLTP_range:
                    min_WLTP_range = ev.WLTP_range
                if max_cost < ev.cost:
                    max_cost = ev.cost
                if min_cost > ev.cost:
                    min_cost = ev.cost
                if max_power < ev.power:
                    max_power = ev.power
                if min_power > ev.power:
                    min_power = ev.power
                if ev.rating:
                    if max_rating < ev.rating:
                        max_rating = ev.rating
                    if min_rating > ev.rating:
                        min_rating = ev.rating


            # values to be rendered to the compare.html page
            template_values = {
            'user': user,
            'q' : q,
            'EVs' : EVs,
            'error' : error,
            'max_battery_size' : max_battery_size,
            'min_battery_size' : min_battery_size,
            'max_WLTP_range' : max_WLTP_range,
            'min_WLTP_range' : min_WLTP_range,
            'max_cost' : max_cost,
            'min_cost' : min_cost,
            'max_power' : max_power,
            'min_power' : min_power,
            'max_rating' : max_rating,
            'min_rating' : min_rating
            }

            template = JINJA_ENVIRONMENT.get_template('compare.html')
            self.response.write(template.render(template_values))

        elif action == 'Cancel':
            self.redirect('/')
