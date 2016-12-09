from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..models.comment import Comment
from ..models.user import User
from ..constants import BLOG_KEY, COMMENT_KEY


class BlogFrontHandler(BlogHandler):
    """Front page of the blog"""
    def get(self):
        """Renders multiple blog posts"""

        error = self.request.get("error")
        # Fetch the top 10 most recently created blog posts from the DB
        query = BlogPost.all().ancestor(BLOG_KEY).order("-createdTime")
        blog_posts = query.fetch(limit=10)
        comments = []
        creators = []
        if blog_posts:
            user_id = self.user.key().id() if self.user else None
            liked_posts = self.user.liked_posts if self.user else None
            for blog_post in blog_posts:
                comments.append(Comment.get_by_id(blog_post.comment_ids,
                                                  parent=COMMENT_KEY))
                creators.append(User.get_by_id(blog_post.user_id).username)

            self.render("blog_post.html",
                        blog_posts=blog_posts,
                        comments=comments,
                        error=error,
                        liked_posts=liked_posts,
                        creators=creators,
                        user_id=user_id)
        else:
            self.render("blog_post.html", error=error, blog_posts=[], comments=[])
