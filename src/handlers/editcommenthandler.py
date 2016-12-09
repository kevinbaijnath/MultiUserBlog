from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY


class EditCommentHandler(BlogHandler):
    """Defines the Delete Comment functionality"""
    def post(self, blog_id, comment_id):
        """Removes the comment from the blog post"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        comment = Comment.get_by_id(int(comment_id), parent=COMMENT_KEY)
        content = self.request.get("edit_comment_content")

        if not (blog_post and comment):
            self.error(404)
            self.render("404.html")

        if not self.user or self.user.key().id() != comment.user_id:
            return self.redirect("/login")

        int_comment_id = int(comment_id)

        if int_comment_id not in blog_post.comment_ids:
            self.error(404)
            self.render("404.html")

        comment.content = content
        comment.put()

        self.redirect("/blog/{0}".format(blog_id))
