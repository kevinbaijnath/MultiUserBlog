from ..handlers.bloghandler import BlogHandler
from ..constants import USER_RE, PASSWORD_RE
from ..models.user import User


class LoginHandler(BlogHandler):
    """Defines the login functionality"""
    def get(self):
        """Shows the login page"""
        self.render("login.html")

    def post(self):
        """Logs in the user"""
        username = self.request.get("username")
        password = self.request.get("password")

        error_username = not USER_RE.match(username)
        error_password = not PASSWORD_RE.match(password)
        user = User.login_user(username, password)

        if error_username or error_password or not user:
            if error_username:
                error_message = "You did not enter a valid username"
            elif error_password:
                error_message = "You did not enter a valid password"
            elif not user:
                error_message = """Unable to find a user
                                   with that username or password"""
            else:
                error_message = "Something went wrong!"
            self.render("login.html", username=username, error=error_message)
        else:
            self.login(user)
            self.redirect("/welcome")
