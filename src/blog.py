"""
Contains the WebApphandlers for the MultiUserBlog
"""
import webapp2

from handlers.mainhandler import MainHandler
from handlers.blogfronthandler import BlogFrontHandler
from handlers.newblogposthandler import NewBlogPostHandler
from handlers.blogposthandler import BlogPostHandler
from handlers.editblogposthandler import EditBlogPostHandler
from handlers.deleteblogposthandler import DeleteBlogPostHandler
from handlers.starblogposthandler import StarBlogPostHandler
from handlers.unstarblogposthandler import UnstarBlogPostHandler
from handlers.starredblogposthandler import StarredBlogPostHandler
from handlers.newcommenthandler import NewCommentHandler
from handlers.deletecommenthandler import DeleteCommentHandler
from handlers.registrationhandler import RegistrationHandler
from handlers.welcomehandler import WelcomeHandler
from handlers.logouthandler import LogoutHandler
from handlers.loginhandler import LoginHandler

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
