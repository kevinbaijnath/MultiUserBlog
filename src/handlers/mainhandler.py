import webapp2


class MainHandler(webapp2.RequestHandler):
    """Main Handler for the blog"""

    def get(self):
        """Redirects to the blog page"""
        self.redirect("/blog")
