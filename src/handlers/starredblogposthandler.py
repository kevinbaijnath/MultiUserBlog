from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..models.user import User
from ..constants import BLOG_KEY, COMMENT_KEY


class StarredBlogPostHandler(BlogHandler):
    """Defines the Starred Post functionality"""
    def get(self):
        """Displays all of the users starred posts"""
        if not self.user:
            return self.redirect("/login")

        blog_posts = []
        comments = []
        creators = []
        for blog_id in self.user.liked_posts:
            blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
            if blog_post:
                blog_posts.append(blog_post)
                comments.append(Comment.get_by_id(blog_post.comment_ids,
                                                  parent=COMMENT_KEY))
                creators.append(User.get_by_id(blog_post.user_id).username)

        self.render("blog_post.html",
                    blog_posts=blog_posts,
                    comments=comments,
                    user_id=self.user.key().id(),
                    creators=creators,
                    liked_posts=self.user.liked_posts)
