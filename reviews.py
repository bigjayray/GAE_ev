import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os

from review import Review
from ev import EV
from review import Review

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True
)

class Reviews(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        user = users.get_current_user()

        q = EV.query()

        template_values = {
            'user': user,
            'q' : q
        }

        template = JINJA_ENVIRONMENT.get_template('reviews.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        action = self.request.get('button')

        new_review = Review()

        if action == 'Submit':
            ev_id = self.request.get('ev')
            new_review.comment = self.request.get('comment')
            new_review.rating = int(self.request.get('rating'))

            key = ndb.Key('EV', int(ev_id))
            ev = key.get()

            ev.reviews.append(new_review)

            count = 0;
            sum = 0;
            average = 0.0;
            for i in ev.reviews:
                sum += i.rating
                count += 1
            average = (sum)/(count)

            ev.rating = average

            ev.put()
            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
