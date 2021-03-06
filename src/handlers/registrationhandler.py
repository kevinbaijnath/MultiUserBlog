from ..constants import USER_RE, PASSWORD_RE, EMAIL_RE
from ..handlers.bloghandler import BlogHandler
from ..models.user import User


class RegistrationHandler(BlogHandler):
    """Registration Page"""

    def get(self):
        """Renders the registration page"""
        if self.user:
            self.redirect("/welcome")
        else:
            self.render("register.html")

    def post(self):
        """Registers the user"""
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        error_username = not USER_RE.match(username)
        error_password = not PASSWORD_RE.match(password)
        error_verify = password != verify
        error_email = email and not EMAIL_RE.match(email)

        if error_username or error_password or error_verify or error_email:
            if error_username:
                error_message = "Usernames must be between 3 and 20 characters"
            elif error_password:
                error_message = "Passwords must be between 3 and 20 characters"
            elif error_verify:
                error_message = "The verify password did not match password"
            else:
                error_message = "The email entered was not a valid email"
            self.render("register.html",
                        username=username,
                        email=email,
                        error=error_message)
        else:
            if User.find_by_username(username):
                error_message = "Someone already has this username!"
                self.render("register.html",
                            username=username,
                            email=email,
                            error=error_message)
            else:
                newuser = User.register(username, password, email)
                newuser.put()
                self.login(newuser)
                self.redirect("/welcome")
