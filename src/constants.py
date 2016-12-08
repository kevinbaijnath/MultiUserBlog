"""
This is used as the ancestor key to get around the issue of eventual consistency in GAE
See https://goo.gl/j2fUa4 for more info
"""
import re
from google.appengine.ext import db

BLOG_KEY = db.Key.from_path('blogs', 'default')
COMMENT_KEY = db.Key.from_path('comments', 'default')
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
