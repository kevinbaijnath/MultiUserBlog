"""
Contains the WebAppHandlers for the MultiUserBlog
"""

import os
#import re
#import random
#import hashlib
#import hmac
#from string import letters

import webapp2
import jinja2
import logging

from google.appengine.ext import db

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), "templates")
JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR),
                               autoescape=True)
SECRET = 'fart'

class BlogPost(db.Model):
    """Defines the model for each blog post"""
    subject = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    createdTime = db.DateTimeProperty(auto_now_add=True)
    #Using auto_now to update the date each time the object is updated
    updatedDate = db.DateProperty(auto_now=True)

    @classmethod
    def create_blog(self):
        pass

def render_str(template, **params):
    """Renders a template along with any parameters as a string"""
    template = JINJA_ENV.get_template(template)
    return template.render(params)


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

    def __init__(self, *args, **kwargs):
        self.user = None
        super(BlogHandler, self).__init__(*args, **kwargs)

class MainHandler(webapp2.RequestHandler):
    """Main Handler for the blog"""
    def get(self):
        """Redirects to the blog page"""
        self.redirect("/blog")

class BlogFrontHandler(BlogHandler):
    """Front page of the blog"""
    def get(self):
        """Renders multiple blog posts"""
        blog_posts = BlogPost.gql("ORDER BY createdTime DESC").fetch(limit=10)

        if blog_posts:
            self.render("blog_post.html", blog_posts=blog_posts)
        else:
            self.error(404)

class NewBlogPostHandler(BlogHandler):
    """New blog post page"""
    def get(self):
        """Render the new blog post page"""
        self.render("create_post.html", error="")

    def post(self):
        """NewBlogPost form submission"""
        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html", error="Please enter a subject!", content=content)
        elif not content:
            self.render("create_post.html", error="Please enter some content!", subject=subject)
        else:
            post = BlogPost(subject=subject, content=content)
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))

class BlogPostHandler(BlogHandler):
    """Blog Post Page"""

    def get(self, blog_id):
        """Renders a Blog Post Page based on the ID"""
        if not blog_id.isdigit():
            self.error(404)

        blog_post = BlogPost.get_by_id(int(blog_id))

        if blog_post:
            self.render("blog_post.html", blog_posts=[blog_post])
        else:
            self.error(404)

app = webapp2.WSGIApplication([("/", MainHandler),
                               ("/blog/?", BlogFrontHandler),
                               ("/blog/newpost", NewBlogPostHandler),
                               (r"/blog/(\d+)", BlogPostHandler)
                              ],
                              debug=True)

"""
('/blog/([0-9]+)', PostPage),
                               ('/blog/newpost', NewPost),
                               ('/signup', Register),
                               ('/login', Login),
                               ('/logout', Logout),
                               ('/unit3/welcome', Unit3Welcome),"""
