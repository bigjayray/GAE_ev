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

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Typ'] = 'text/html'

        url = ''
        url_string = ''
        welcome = 'Welcome back'
        myuser = None

        user = users.get_current_user()

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

        template_values = {
            'url' : url,
            'url_string' : url_string,
            'user' : user,
            'welcome' : welcome,
            'myuser' : myuser
        }

        template = JINJA_ENVIRONMENT.get_template('main.html')
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

            template = JINJA_ENVIRONMENT.get_template('main.html')
            self.response.write(template.render(template_values))

            # if name == None or name == '' or manufacturer == None or manufacturer == '' or year == None or battery_size == None or WLTP_range == None or cost == None or power == None:
            #     self.redirect('/')
            #     return

            # query = EV.query(ndb.OR(EV.manufacturer == manufacturer, EV.name == name, EV.year == year,
            # EV.battery_size == battery_size, EV.WLTP_range == WLTP_range, EV.cost == cost, EV.power == power))

            # for i in q:
            #     self.response.write(i.name + '<br/>')

# starts the web application and specify the full routing table here as well
app = webapp2.WSGIApplication([
    ('/', MainPage),
    ('/addev', AddEv),
    ('/details', Details),
], debug=True)
