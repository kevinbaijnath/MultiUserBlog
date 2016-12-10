from ..constants import BLOG_KEY, COMMENT_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import (blogpost_exists,
                                  comment_exists_in_blogpost,
                                  logged_in,
                                  user_authorized_comment)
from ..models.blogpost import BlogPost
from ..models.comment import Comment


class EditCommentHandler(BlogHandler):
    """Defines the Delete Comment functionality"""

    @logged_in
    @blogpost_exists
    @comment_exists_in_blogpost
    @user_authorized_comment
    def post(self, blog_id, comment_id):
        """Removes the comment from the blog post"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        comment = Comment.get_by_id(int(comment_id), parent=COMMENT_KEY)
        content = self.request.get("edit_comment_content")

        comment.content = content
        comment.put()

        self.redirect("/blog/{0}".format(blog_id))
