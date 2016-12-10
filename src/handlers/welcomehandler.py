from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import logged_in


class WelcomeHandler(BlogHandler):
    """Defines the WelcomePage for the logged in user"""

    @logged_in
    def get(self):
        """Renders the welcome.html page"""
        self.render("welcome.html", username=self.user.username)
