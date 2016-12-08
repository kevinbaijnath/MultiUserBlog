from google.appengine.ext import db
from ..helpers.securepassword import SecurePassword

class User(db.Model):
    """Defines the model for users"""
    username = db.StringProperty(required=True)
    passwordHash = db.StringProperty(required=True)
    email = db.StringProperty()
    createdTime = db.DateTimeProperty(auto_now_add=True)
    liked_posts = db.ListProperty(int, default=[])

    @classmethod
    def register(cls, username, password, email):
        """Creates a new user object"""
        hashed_password = SecurePassword.make_password_hash(username, password)
        return User(username=username, passwordHash=hashed_password, email=email)

    @classmethod
    def find_by_username(cls, username):
        """Returns a user object given a specific username"""
        return User.all().filter('username =', username).get()

    @classmethod
    def login_user(cls, username, password):
        """Verifies inputted credentials against db"""
        user = cls.find_by_username(username)

        if user and SecurePassword.valid_password(username, password, user.passwordHash):
            return user
        else:
            return None
