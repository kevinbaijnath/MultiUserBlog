from ..constants import BLOG_KEY, COMMENT_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import logged_in, blogpost_exists
from ..models.blogpost import BlogPost
from ..models.comment import Comment


class NewCommentHandler(BlogHandler):
    """Defines the New Comment functionality"""

    @logged_in
    @blogpost_exists
    def post(self, blog_id):
        """Defines the creating comment functionality"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        content = self.request.get("comment_content")
        comment = Comment(content=content,
                          user_id=self.user.key().id(),
                          username=self.user.username,
                          parent=COMMENT_KEY)
        comment.put()
        blog_post.comment_ids.append(comment.key().id())
        blog_post.put()
        self.redirect("/blog/{0}".format(blog_id))
