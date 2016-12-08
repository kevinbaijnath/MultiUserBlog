"""
Contains the WebAppHandlers for the MultiUserBlog
"""
import webapp2

from src.handlers.mainhandler import MainHandler
from src.handlers.blogfronthandler import BlogFrontHandler
from src.handlers.newblogposthandler import NewBlogPostHandler
from src.handlers.blogposthandler import BlogPostHandler
from src.handlers.editblogposthandler import EditBlogPostHandler
from src.handlers.deleteblogposthandler import DeleteBlogPostHandler
from src.handlers.starblogposthandler import StarBlogPostHandler
from src.handlers.unstarblogposthandler import UnstarBlogPostHandler
from src.handlers.starredblogposthandler import StarredBlogPostHandler
from src.handlers.newcommenthandler import NewCommentHandler
from src.handlers.deletecommenthandler import DeleteCommentHandler
from src.handlers.registrationhandler import RegistrationHandler
from src.handlers.welcomehandler import WelcomeHandler
from src.handlers.logouthandler import LogoutHandler
from src.handlers.loginhandler import LoginHandler

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
