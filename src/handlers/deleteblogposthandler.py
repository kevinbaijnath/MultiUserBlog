from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..constants import BLOG_KEY, COMMENT_KEY

class DeleteBlogPostHandler(BlogHandler):
    """Defines the delete blog functionality"""
    def get(self, blog_id):
        """"Deletes the blog post if the user is authorized"""
        if not self.user:
            self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

        #Check to make sure that the user is authorized to delete this post
        if not blog_post or not blog_post.user_id != self.user.key().id():
            self.redirect("/login")

        #We need to remove the comments as well to preven them from being orphaned
        comments = Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY)
        for comment in comments:
            if comment:
                comment.delete()

        blog_post.delete()
        self.redirect("/blog")
