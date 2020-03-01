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

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        if action == 'Edit':

            q_name = self.request.get('name')
            q_manufacturer = self.request.get('manufacturer')
            q_year = int(self.request.get('year'))

            name = self.request.get('ev_name')
            manufacturer = self.request.get('ev_manufacturer')
            year = int(self.request.get('ev_year'))
            battery_size = float(self.request.get('ev_battery_size'))
            WLTP_range = float(self.request.get('ev_WLTP_range'))
            cost = float(self.request.get('ev_cost'))
            power = float(self.request.get('ev_power'))

            query = EV.query(ndb.AND(EV.manufacturer == q_manufacturer, EV.name == q_name, EV.year == q_year))

            print(query.count())
            if query.count(1) == 1:
                for ev in query:
                    ev.name = name
                    ev.manufacturer = manufacturer
                    ev.year = year
                    ev.battery_size = battery_size
                    ev.WLTP_range = WLTP_range
                    ev.cost = cost
                    ev.power = power
                    ev.put()
                    print('hello world')

            # for i in query:
            # ev = i


            self.redirect('/')

        elif action == 'Delete':
            name = self.request.get('ev_name')
            manufacturer = self.request.get('ev_manufacturer')
            year = int(self.request.get('ev_year'))

            query = EV.query(ndb.AND(EV.manufacturer == manufacturer, EV.name == name, EV.year == year))

            if query.count(1) == 1:
                for ev in query:
                    ev.key.delete()
            self.redirect('/')
        elif action == 'Cancel':
            self.redirect('/')
