from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..constants import BLOG_KEY

class NewBlogPostHandler(BlogHandler):
    """New blog post page"""

    def get(self):
        """Render the new blog post page"""
        if not self.user:
            self.redirect("/login")

        self.render("create_post.html", error="")

    def post(self):
        """NewBlogPost form submission"""
        if not self.user:
            self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html", error="Please enter a subject!", content=content)
        elif not content:
            self.render("create_post.html", error="Please enter some content!", subject=subject)
        else:
            post = BlogPost(subject=subject,
                            content=content,
                            user_id=self.user.key().id(),
                            parent=BLOG_KEY)
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))
