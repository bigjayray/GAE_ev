# imports
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

# Reviews Class
class Reviews(webapp2.RequestHandler):
    # get method called on page when page is instantiated
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'

        # get current user
        user = users.get_current_user()

        # query datastore for evs
        q = EV.query()

        # values to be rendered to the reviews.html page
        template_values = {
            'user': user,
            'q' : q
        }

        template = JINJA_ENVIRONMENT.get_template('reviews.html')
        self.response.write(template.render(template_values))

    # called when you submit a web form
    def post(self):
        self.response.headers['Content-Type'] = 'text/html'

        # get value of button clicked
        action = self.request.get('button')

        # create new review object
        new_review = Review()

        # selection statement for button
        if action == 'Submit':
            # gets id from form
            ev_id = self.request.get('ev')
            new_review.comment = self.request.get('comment')
            new_review.rating = int(self.request.get('rating'))

            # generates key
            key = ndb.Key('EV', int(ev_id))
            ev = key.get()

            ev.reviews.append(new_review)

            # calculates average rating
            count = 0;
            sum = 0;
            average = 0.0;
            for i in ev.reviews:
                sum += i.rating
                count += 1
            average = (sum)/(count)

            ev.rating = average

            # updates ev
            ev.put()
            self.redirect('/')

        elif action == 'Cancel':
            self.redirect('/')
