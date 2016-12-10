import urllib
from ..constants import BLOG_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import logged_in, blogpost_exists
from ..models.blogpost import BlogPost


class StarBlogPostHandler(BlogHandler):
    """Defines the Blog Post like/star functionality"""

    @logged_in
    @blogpost_exists
    def get(self, blog_id):
        """Add the blog post to the user's liked/starred posts"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        if blog_post.user_id != self.user.key().id():
            self.user.liked_posts.append(int(blog_id))
            self.user.put()
            self.redirect("/blog/"+blog_id)
        else:
            safe_url = urllib.quote("You can't like your own posts!")
            path = "/blog/"+blog_id+"?error="+safe_url
            self.redirect(path)
