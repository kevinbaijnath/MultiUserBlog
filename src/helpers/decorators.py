import urllib
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY


def logged_in(func):
    """Checks to see if the user object has been set (logged in)"""
    def wrapper(self, *args, **kwargs):
        if not self.user:
            return self.redirect("/login")
        return func(self, *args, **kwargs)
    return wrapper


def blogpost_exists(func):
    """Checks to make sure that the blogpost exists or renders 404"""
    def wrapper(self, blog_id, *args, **kwargs):
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        if not blog_post:
            self.error(404)
            return self.render("404.html")
        return func(self, blog_id, *args, **kwargs)
    return wrapper


def user_authorized_blogpost(func):
    """Checks to make sure the user id matches blog user id"""
    def wrapper(self, blog_id, *args, **kwargs):
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        if self.user.key().id() != blog_post.user_id:
            error = urllib.quote("You can't modify that blogpost!")
            return self.redirect("/blog?error="+error)
        return func(self, blog_id, *args, **kwargs)
    return wrapper


def comment_exists_in_blogpost(func):
    """Checks to make sure the comment exists or renders a 404"""
    def wrapper(self, blog_id, comment_id, *args, **kwargs):
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        int_comment_id = int(comment_id)
        comment = Comment.get_by_id(int_comment_id, parent=COMMENT_KEY)

        exists = blog_post and comment
        contains_comment = int_comment_id in blog_post.comment_ids
        if not exists or not contains_comment:
            self.error(404)
            return self.render("404.html")
        return func(self, blog_id, comment_id, *args, **kwargs)
    return wrapper


def user_authorized_comment(func):
    """Checks to make sure the user id matches the comment user id"""
    def wrapper(self, blog_id, comment_id, *args, **kwargs):
        comment = Comment.get_by_id(int(comment_id), parent=COMMENT_KEY)
        if not self.user.key().id() == comment.user_id:
            error = urllib.quote("You can't modify that comment!")
            return self.redirect("/blog?error="+error)
        return func(self, blog_id, comment_id, *args, **kwargs)
    return wrapper
