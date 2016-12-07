"""
Contains the WebAppHandlers for the MultiUserBlog
"""

import os
#import re
#import random
#import hashlib
#import hmac
#from string import letters

import logging

import hashlib
import hmac
import urllib
import random
import re
from string import letters
import jinja2
import webapp2

from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

SECRET = 'thisisasecurestringvalue'

"""
This is used as the ancestor key to get around the issue of eventual consistency in GAE
See https://goo.gl/j2fUa4 for more info
"""
BLOG_KEY = db.Key.from_path('blogs', 'default')
COMMENT_KEY = db.Key.from_path('comments', 'default')

class BlogPost(db.Model):
    """Defines the model for each blog post"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    createdTime = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(required=True)
    #Using auto_now to update the date each time the object is updated
    updatedDate = db.DateProperty(auto_now=True)
    comment_ids = db.ListProperty(int, default=[])

class Comment(db.Model):
    """Defines the model for each comment"""
    content = db.TextProperty(required=True)
    createdTime = db.DateTimeProperty(auto_now_add=True)
    user_id = db.IntegerProperty(required=True)
    username = db.StringProperty(required=True)

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

def render_str(template, **params):
    """Renders a template along with any parameters as a string"""
    template = JINJA_ENV.get_template(template)
    return template.render(params)

class SecureString(object):
    """Secure String implementation"""
    @classmethod
    def make_secure_val(cls, plain_string):
        """Returns a secure string from an input string"""
        return "%s|%s" % (plain_string, hmac.new(SECRET, plain_string).hexdigest())

    @classmethod
    def check_secure_val(cls, secure_val):
        """Checks to see if the input is valid"""
        inp = secure_val.split('|')[0]
        return inp and (secure_val == cls.make_secure_val(inp))

    @classmethod
    def get_userid(cls, secure_string):
        """Gets the user id from a secure string"""
        return secure_string.split('|')[0] if secure_string else None

    @classmethod
    def is_valid_cookie(cls, inp_string):
        """Takes in a string and checks to see if it is a valid secure string"""
        return inp_string and cls.check_secure_val(inp_string)

class SecurePassword(object):
    """Secure Password implementation"""
    @classmethod
    def make_salt(cls, length=5):
        """Creates a salt that is 5 random letters joined together"""
        return ''.join(random.choice(letters) for x in xrange(length))

    @classmethod
    def make_password_hash(cls, name, password, salt=None):
        """Creates a password hash based off a given salt (or a new salt)"""
        if not salt:
            salt = cls.make_salt()
        new_hash = hashlib.sha256(name + password + salt).hexdigest()
        return "%s,%s" % (salt, new_hash)

    @classmethod
    def valid_password(cls, name, password, new_hash):
        """Checks to see if the input hash is equal to the user password hash"""
        salt = new_hash.split(',')[0]
        return new_hash == cls.make_password_hash(name, password, salt)

class BlogHandler(webapp2.RequestHandler):
    """BaseClass for the Blog"""

    def write(self, *args, **kwargs):
        """Helper method to write out a response"""
        self.response.out.write(*args, **kwargs)

    def render_str(self, template, **params):
        """Passes a user and renders a template as a string"""
        params['user'] = self.user
        return render_str(template, **params)

    def render(self, template, **kwargs):
        """Renders a template"""
        self.write(self.render_str(template, **kwargs))

    def login(self, user):
        """Sets the user_id cookie"""
        secure_string = SecureString.make_secure_val(str(user.key().id()))
        cookie_val = 'user_id={0}; Path=/'.format(secure_string)
        self.response.headers.add_header('Set-Cookie', cookie_val)

    def logout(self):
        """Logs the user out by emptying the cookie"""
        self.response.headers.add_header('Set-Cookie', 'user_id=; Path=/')

    def __init__(self, *args, **kwargs):
        self.user = None
        super(BlogHandler, self).__init__(*args, **kwargs)

    def initialize(self, *args, **kwargs):
        """Adds the user to the instance if the user is logged in"""
        webapp2.RequestHandler.initialize(self, *args, **kwargs)
        user_id = SecureString.get_userid(self.request.cookies.get('user_id'))
        if user_id:
            user = User.get_by_id(int(user_id))
            if user:
                self.user = user
            else:
                self.user = None
        else:
            self.user = None

class MainHandler(webapp2.RequestHandler):
    """Main Handler for the blog"""

    def get(self):
        """Redirects to the blog page"""
        self.redirect("/blog")

class BlogFrontHandler(BlogHandler):
    """Front page of the blog"""
    def get(self):
        """Renders multiple blog posts"""

        error = self.request.get("error")
        logging.error(error)
        blog_posts = BlogPost.all().ancestor(BLOG_KEY).order("-createdTime").fetch(limit=10)
        comments = []
        if blog_posts:
            user_id = self.user.key().id() if self.user else None
            liked_posts = self.user.liked_posts if self.user else None
            for blog_post in blog_posts:
                comments.append(Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY))

            self.render("blog_post.html",
                        blog_posts=blog_posts,
                        comments=comments,
                        error=error,
                        liked_posts=liked_posts,
                        user_id=user_id)
        else:
            self.render("blog_post.html", error=error, blog_posts=[], comments=[])

class NewBlogPostHandler(BlogHandler):
    """New blog post page"""

    def get(self):
        """Render the new blog post page"""
        if not self.user:
            self.redirect("/login")

        self.render("create_post.html", error="")

    def post(self):
        """NewBlogPost form submission"""
        if not self.user:
            self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html", error="Please enter a subject!", content=content)
        elif not content:
            self.render("create_post.html", error="Please enter some content!", subject=subject)
        else:
            post = BlogPost(subject=subject,
                            content=content,
                            user_id=self.user.key().id(),
                            parent=BLOG_KEY)
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))

class BlogPostHandler(BlogHandler):
    """Blog Post Page"""

    def get(self, blog_id):
        """Renders a Blog Post Page based on the ID"""
        if not blog_id.isdigit():
            self.error(404)

        error = self.request.get("error")
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        comments = Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY)
        if blog_post:
            if self.user:
                self.render("blog_post.html",
                            blog_posts=[blog_post],
                            comments=[comments],
                            error=error,
                            user_id=self.user.key().id(),
                            liked_posts=self.user.liked_posts)
            else:
                self.render("blog_post.html",
                            blog_posts=[blog_post],
                            comments=[comments],
                            user_id=None,
                            error=error)
        else:
            self.error(404)

class EditBlogPostHandler(BlogHandler):
    """Defines the edit blog functionality"""
    def get(self, blog_id):
        """Shows the user the edit blog page"""
        if not self.user:
            self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

        logging.error(blog_post.subject)
        if not blog_post:
            self.error(404)

        self.render("create_post.html", content=blog_post.content, subject=blog_post.subject)

    def post(self, blog_id):
        """Updates the post"""
        if not self.user:
            self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html", error="Please enter a subject!", content=content)
        elif not content:
            self.render("create_post.html", error="Please enter some content!", subject=subject)
        else:
            post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))

class DeleteBlogPostHandler(BlogHandler):
    """Defines the delete blog functionality"""
    def get(self, blog_id):
        """"Deletes the blog post if the user is authorized"""
        if not self.user:
            self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

        #Check to make sure that the user is authorized to delete this post
        if not blog_post or not blog_post.user_id != self.user.key().id():
            self.redirect("/login")

        #We need to remove the comments as well to preven them from being orphaned
        comments = Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY)
        for comment in comments:
            if comment:
                comment.delete()

        blog_post.delete()
        self.redirect("/blog")

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
        has_error = error_username or error_password or error_verify or error_email

        if has_error:
            if error_username:
                error_message = "Your username must be alphanumeric between 3 and 20 characters"
            elif error_password:
                error_message = "Your password must be between 3 and 20 characters"
            elif error_verify:
                error_message = "The verify password did not match the password you typed in"
            else:
                error_message = "The email that you entered was not a valid email"

            self.render("register.html", username=username, email=email, error=error_message)

        if User.find_by_username(username):
            error_message = "Someone already has this username"
            self.render("register.html", username=username, email=email, error=error_message)
        else:
            newuser = User.register(username, password, email)
            newuser.put()
            self.login(newuser)
            self.redirect("/welcome")

class WelcomeHandler(BlogHandler):
    """Defines the WelcomePage for the logged in user"""
    def get(self):
        """Renders the welcome.html page"""
        if self.user:
            self.render("welcome.html", username=self.user.username)
        else:
            self.redirect("/login")

class LogoutHandler(BlogHandler):
    """Defines the logout functionality"""
    def get(self):
        """Logs out the user"""
        self.logout()
        self.redirect("/blog")

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

        if error_username or error_password:
            if error_username:
                error_message = "Your username must be alphanumeric between 3 and 20 characters"
            else:
                error_message = "Your password must be between 3 and 20 characters"

        user = User.login_user(username, password)
        if user:
            self.login(user)
            self.redirect("/welcome")
        else:
            error_message = "We were unable to find a user with that username or password"
            self.render("login.html", username=username, error=error_message)

class StarBlogPostHandler(BlogHandler):
    """Defines the Blog Post like/star functionality"""
    def get(self, blog_id):
        """Add the blog post to the user's liked/starred posts"""
        if not self.user:
            self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        if blog_post:
            if blog_post.user_id != self.user.key().id():
                self.user.liked_posts.append(int(blog_id))
                self.user.put()
                self.redirect("/blog/"+blog_id)
            else:
                path = "/blog/"+blog_id+"?error="+urllib.quote("You can't like your own posts!")
                self.redirect(path)
        else:
            self.error(404)

class UnstarBlogPostHandler(BlogHandler):
    """Defines the Blog Post unlike/unstar functionality"""
    def get(self, blog_id):
        """Remove the blog post from the user's liked/starred posts"""
        if not self.user:
            self.redirect("/login")

        int_blog_id = int(blog_id)
        blog_post = BlogPost.get_by_id(int_blog_id, parent=BLOG_KEY)
        if blog_post:
            logging.error("found blog post!")
            if int_blog_id in self.user.liked_posts:
                self.user.liked_posts.remove(int_blog_id)
                self.user.put()
                self.redirect("/blog/"+blog_id)
            else:
                base_path = "/blog/"+blog_id+"?error="
                error_path = urllib.quote("You can't unstar posts that you haven't starred!")
                self.redirect(base_path+error_path)
        else:
            logging.error("coulnd't find blog post")
            self.error(404)

class StarredBlogPostHandler(BlogHandler):
    """Defines the Starred Post functionality"""
    def get(self):
        """Displays all of the users starred posts"""
        if not self.user:
            self.redirect("/login")

        blog_posts = []
        comments = []
        for blog_id in self.user.liked_posts:
            blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
            if blog_post:
                blog_posts.append(blog_post)
                comments.append(Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY))

        self.render("blog_post.html",
                    blog_posts=blog_posts,
                    comments=comments,
                    user_id=self.user.key().id(),
                    liked_posts=self.user.liked_posts)

class NewCommentHandler(BlogHandler):
    """Defines the New Comment functionality"""
    def post(self, blog_id):
        """Defines the creating comment functionality"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        content = self.request.get("comment_content")
        if self.user and blog_post:
            comment = Comment(content=content,
                              user_id=self.user.key().id(),
                              username=self.user.username,
                              parent=COMMENT_KEY)
            comment.put()
            blog_post.comment_ids.append(comment.key().id())
            blog_post.put()
            self.redirect("/blog/{0}".format(blog_id))
        else:
            self.error(404)

class DeleteCommentHandler(BlogHandler):
    """Defines the Delete Comment functionality"""
    def get(self, blog_id, comment_id):
        """Removes the comment from the blog post"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        comment = Comment.get_by_id(int(comment_id), parent=COMMENT_KEY)

        if not (blog_post and comment):
            self.error(404)

        int_comment_id = int(comment_id)

        if not int_comment_id in blog_post.comment_ids:
            self.error(404)

        blog_post.comment_ids.remove(int_comment_id)
        blog_post.put()
        comment.delete()

        self.redirect("/blog/{0}".format(blog_id))

app = webapp2.WSGIApplication([("/", MainHandler),
                               (r"/blog/?", BlogFrontHandler),
                               ("/blog/newpost/?", NewBlogPostHandler),
                               (r"/blog/(\d+)/?", BlogPostHandler),
                               (r"/blog/edit/(\d+)/?", EditBlogPostHandler),
                               (r"/blog/delete/(\d+)/?", DeleteBlogPostHandler),
                               (r"/blog/star/(\d+)/?", StarBlogPostHandler),
                               (r"/blog/unstar/(\d+)/?", UnstarBlogPostHandler),
                               ("/blog/starred", StarredBlogPostHandler),
                               (r"/blog/newcomment/(\d+)/?", NewCommentHandler),
                               (r"/blog/deletecomment/(\d+)/(\d+)/?", DeleteCommentHandler),
                               ("/register/?", RegistrationHandler),
                               ("/welcome/?", WelcomeHandler),
                               ("/logout/?", LogoutHandler),
                               ("/login/?", LoginHandler)
                              ],
                              debug=True)
