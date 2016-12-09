from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY


class NewCommentHandler(BlogHandler):
    """Defines the New Comment functionality"""
    def post(self, blog_id):
        """Defines the creating comment functionality"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        content = self.request.get("comment_content")
        if self.user and blog_post:
            comment = Comment(content=content,
                              user_id=self.user.key().id(),
                              username=self.user.username,
                              parent=COMMENT_KEY)
            comment.put()
            blog_post.comment_ids.append(comment.key().id())
            blog_post.put()
            self.redirect("/blog/{0}".format(blog_id))
        else:
            self.error(404)
            self.render("404.html")
