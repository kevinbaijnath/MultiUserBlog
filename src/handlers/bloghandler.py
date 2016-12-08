import os
import jinja2
import webapp2

from ..helpers.securestring import SecureString
from ..models.user import User

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "templates")
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)

def render_str(template, **params):
    """Renders a template along with any parameters as a string"""
    template = JINJA_ENV.get_template(template)
    return template.render(params)

class BlogHandler(webapp2.RequestHandler):
    """BaseClass for the Blog"""

    def write(self, *args, **kwargs):
        """Helper method to write out a response"""
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        """Passes a user and renders a template as a string"""
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kwargs):
        """Renders a template"""
        self.write(self.render_str(template, **kwargs))

    def login(self, user):
        """Sets the user_id cookie"""
        secure_string = SecureString.make_secure_val(str(user.key().id()))
        cookie_val = 'user_id={0}; Path=/'.format(secure_string)
        self.response.headers.add_header('Set-Cookie', cookie_val)

    def logout(self):
        """Logs the user out by emptying the cookie"""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def __init__(self, *args, **kwargs):
        self.user = None
        super(BlogHandler, self).__init__(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        """Adds the user to the instance if the user is logged in"""
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        user_id = SecureString.get_userid(self.request.cookies.get('user_id'))
        if user_id:
            user = User.get_by_id(int(user_id))
            if user:
                self.user = user
            else:
                self.user = None
        else:
            self.user = None
