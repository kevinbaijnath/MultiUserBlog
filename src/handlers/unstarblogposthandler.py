import urllib
from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..constants import BLOG_KEY

class UnstarBlogPostHandler(BlogHandler):
    """Defines the Blog Post unlike/unstar functionality"""
    def get(self, blog_id):
        """Remove the blog post from the user's liked/starred posts"""
        if not self.user:
            self.redirect("/login")

        int_blog_id = int(blog_id)
        blog_post = BlogPost.get_by_id(int_blog_id, parent=BLOG_KEY)
        if blog_post:
            if int_blog_id in self.user.liked_posts:
                self.user.liked_posts.remove(int_blog_id)
                self.user.put()
                self.redirect("/blog/"+blog_id)
            else:
                base_path = "/blog/"+blog_id+"?error="
                error_path = urllib.quote("You can't unstar posts that you haven't starred!")
                self.redirect(base_path+error_path)
        else:
            self.error(404)
