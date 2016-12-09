import urllib
from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..constants import BLOG_KEY


class StarBlogPostHandler(BlogHandler):
    """Defines the Blog Post like/star functionality"""
    def get(self, blog_id):
        """Add the blog post to the user's liked/starred posts"""
        if not self.user:
            return self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        if blog_post:
            if blog_post.user_id != self.user.key().id():
                self.user.liked_posts.append(int(blog_id))
                self.user.put()
                self.redirect("/blog/"+blog_id)
            else:
                safe_url = urllib.quote("You can't like your own posts!")
                path = "/blog/"+blog_id+"?error="+safe_url
                self.redirect(path)
        else:
            self.error(404)
            self.render("404.html")
