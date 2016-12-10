from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY
from ..helpers.decorators import (blogpost_exists,
                                  logged_in,
                                  user_authorized_blogpost)


class DeleteBlogPostHandler(BlogHandler):
    """Defines the delete blog functionality"""

    @logged_in
    @blogpost_exists
    @user_authorized_blogpost
    def get(self, blog_id):
        """"Deletes the blog post if the user is authorized"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

        # Comments are being removed to prevent them from being orphaned
        comments = Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY)
        for comment in comments:
            if comment:
                comment.delete()

        blog_post.delete()
        self.redirect("/blog")
