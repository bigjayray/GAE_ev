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
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        q = EV.query()
        ev1 = None
        ev2 = None

        template_values = {
            'user': user,
            'q' : q,
            'ev1' : ev1,
            'ev2' : ev2,
        }

        template = JINJA_ENVIRONMENT.get_template('compare.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()

        action = self.request.get('button')

        if action == 'Compare':
            ev_1 = int(self.request.get('ev_1'))
            ev_2 = int(self.request.get('ev_2'))
            if ev_1 == ev_2:
                self.redirect('/compare')
            else:
                ev1 = EV.get_by_id(ev_1)
                ev2 = EV.get_by_id(ev_2)
                q = EV.query()
            # ids = []
            # for i in q:
            #     ids.append(i.key.id())
            # print(ids)
                template_values = {
                    'user': user,
                    'q' : q,
                    'ev1' : ev1,
                    'ev2' : ev2
                }

                template = JINJA_ENVIRONMENT.get_template('compare.html')
                self.response.write(template.render(template_values))
                
        elif action == 'Cancel':
            self.redirect('/')
