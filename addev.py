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


# AddEv class
class AddEv(webapp2.RequestHandler):

    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # selection statement for user
        if user:
            # values to be rendered to the addev.html page
            template_values = {
                'user': user
            }

            template = JINJA_ENVIRONMENT.get_template('addev.html')
            self.response.write(template.render(template_values))
        else:
            self.redirect('/')

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # gets current user
        user = users.get_current_user()

        # get value of button clicked
        action = self.request.get('button')

        # create a new ev object
        ev = EV()

        # selection statement for button
        if action == 'Add':

            # adds form values to the ev object
            ev.name = self.request.get('ev_name')
            ev.manufacturer = self.request.get('ev_manufacturer')
            ev.year = int(self.request.get('ev_year'))
            ev.battery_size = float(self.request.get('ev_battery_size'))
            ev.WLTP_range = float(self.request.get('ev_WLTP_Range'))
            ev.cost = float(self.request.get('ev_cost'))
            ev.power = float(self.request.get('ev_power'))

            # querys ev to find duplicate ev
            query = EV.query(ndb.AND(EV.manufacturer == ev.manufacturer, EV.name == ev.name, EV.year == ev.year))

            # selection statement for if query count is above 0
            if query.count() > 0:
                error = 'Error: EV already exists!'
                template_values = {
                    'error' : error,
                    'user': user
                }

                template = JINJA_ENVIRONMENT.get_template('addev.html')
                self.response.write(template.render(template_values))
            else:
                # adds ev to datastore
                ev.put()
                self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
