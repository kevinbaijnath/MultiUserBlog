from ..handlers.bloghandler import BlogHandler
from ..models.blogpost import BlogPost
from ..constants import BLOG_KEY

class EditBlogPostHandler(BlogHandler):
    """Defines the edit blog functionality"""
    def get(self, blog_id):
        """Shows the user the edit blog page"""
        if not self.user:
            self.redirect("/login")

        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

        if not blog_post:
            self.error(404)

        self.render("create_post.html",
                    content=blog_post.content,
                    subject=blog_post.subject,
                    blog_id=blog_id)

    def post(self, blog_id):
        """Updates the post"""
        if not self.user:
            self.redirect("/login")

        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html", error="Please enter a subject!", content=content)
        elif not content:
            self.render("create_post.html", error="Please enter some content!", subject=subject)
        else:
            post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))
