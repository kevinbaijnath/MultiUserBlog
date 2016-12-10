import urllib
from ..constants import BLOG_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import logged_in, blogpost_exists
from ..models.blogpost import BlogPost


class UnstarBlogPostHandler(BlogHandler):
    """Defines the Blog Post unlike/unstar functionality"""

    @logged_in
    @blogpost_exists
    def get(self, blog_id):
        """Remove the blog post from the user's liked/starred posts"""
        int_blog_id = int(blog_id)
        blog_post = BlogPost.get_by_id(int_blog_id, parent=BLOG_KEY)

        if int_blog_id in self.user.liked_posts:
            self.user.liked_posts.remove(int_blog_id)
            self.user.put()
            self.redirect("/blog/"+blog_id)
        else:
            base_path = "/blog/"+blog_id+"?error="
            error = urllib.quote("Can't unstar posts that aren't starred")
            self.redirect(base_path+error_path)
