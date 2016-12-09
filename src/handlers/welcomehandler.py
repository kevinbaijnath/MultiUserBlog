from ..handlers.bloghandler import BlogHandler


class WelcomeHandler(BlogHandler):
    """Defines the WelcomePage for the logged in user"""
    def get(self):
        """Renders the welcome.html page"""
        if self.user:
            self.render("welcome.html", username=self.user.username)
        else:
            return self.redirect("/login")
