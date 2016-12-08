from google.appengine.ext import db

class Comment(db.Model):
    """Defines the model for each comment"""
    content = db.TextProperty(required=True)
    createdTime = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)
