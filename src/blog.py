"""
Contains the WebApphandlers for the MultiUserBlog
"""
import webapp2

from handlers.mainhandler import MainHandler
from handlers.blogfronthandler import BlogFrontHandler
from handlers.newblogposthandler import NewBlogPostHandler
from handlers.blogposthandler import BlogPostHandler
from handlers.editblogposthandler import EditBlogPostHandler
from handlers.deleteblogposthandler import DeleteBlogPostHandler as DelBlog
from handlers.starblogposthandler import StarBlogPostHandler
from handlers.unstarblogposthandler import UnstarBlogPostHandler as Unstar
from handlers.starredblogposthandler import StarredBlogPostHandler
from handlers.newcommenthandler import NewCommentHandler as NewComment
from handlers.deletecommenthandler import DeleteCommentHandler as DelCom
from handlers.editcommenthandler import EditCommentHandler as EditCom
from handlers.registrationhandler import RegistrationHandler
from handlers.welcomehandler import WelcomeHandler
from handlers.logouthandler import LogoutHandler
from handlers.loginhandler import LoginHandler

app = webapp2.WSGIApplication([("/", MainHandler),
                               (r"/blog/?", BlogFrontHandler),
                               ("/blog/newpost/?", NewBlogPostHandler),
                               (r"/blog/(\d+)/?", BlogPostHandler),
                               (r"/blog/edit/(\d+)/?", EditBlogPostHandler),
                               (r"/blog/delete/(\d+)/?", DelBlog),
                               (r"/blog/star/(\d+)/?", StarBlogPostHandler),
                               (r"/blog/unstar/(\d+)/?", Unstar),
                               ("/blog/starred", StarredBlogPostHandler),
                               (r"/blog/newcomment/(\d+)/?", NewComment),
                               (r"/blog/deletecomment/(\d+)/(\d+)/?", DelCom),
                               (r"/blog/editcomment/(\d+)/(\d+)/?", EditCom),
                               ("/register/?", RegistrationHandler),
                               ("/welcome/?", WelcomeHandler),
                               ("/logout/?", LogoutHandler),
                               ("/login/?", LoginHandler)
                               ],
                              debug=True)
