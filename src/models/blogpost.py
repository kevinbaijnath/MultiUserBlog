from google.appengine.ext import db


class BlogPost(db.Model):
    """Defines the model for each blog post"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    createdTime = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(required=True)
    # Using auto_now to update the date each time the object is updated
    updatedDate = db.DateProperty(auto_now=True)
    comment_ids = db.ListProperty(int, default=[])
