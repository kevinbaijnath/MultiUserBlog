from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY

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
