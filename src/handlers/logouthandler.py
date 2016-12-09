from ..handlers.bloghandler import BlogHandler


class LogoutHandler(BlogHandler):
    """Defines the logout functionality"""
    def get(self):
        """Logs out the user"""
        self.logout()
        self.redirect("/blog")
