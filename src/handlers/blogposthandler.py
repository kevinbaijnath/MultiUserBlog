from ..constants import BLOG_KEY, COMMENT_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import blogpost_exists
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..models.user import User


class BlogPostHandler(BlogHandler):
    """Blog Post Page"""

    @blogpost_exists
    def get(self, blog_id):
        """Renders a Blog Post Page based on the ID"""
        error = self.request.get("error")
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        comments = Comment.get_by_id(blog_post.comment_ids, parent=COMMENT_KEY)

        username = [User.get_by_id(blog_post.user_id).username]
        if self.user:
            self.render("blog_post.html",
                        blog_posts=[blog_post],
                        comments=[comments],
                        error=error,
                        user_id=self.user.key().id(),
                        creators=username,
                        liked_posts=self.user.liked_posts)
        else:
            self.render("blog_post.html",
                        blog_posts=[blog_post],
                        comments=[comments],
                        creators=username,
                        user_id=None,
                        error=error)
