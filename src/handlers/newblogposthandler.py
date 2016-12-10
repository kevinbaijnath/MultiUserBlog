from ..constants import BLOG_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import logged_in
from ..models.blogpost import BlogPost


class NewBlogPostHandler(BlogHandler):
    """New blog post page"""

    @logged_in
    def get(self):
        """Render the new blog post page"""
        self.render("create_post.html", error="")

    @logged_in
    def post(self):
        """NewBlogPost form submission"""

        subject = self.request.get("subject")
        content = self.request.get("content")

        if not subject:
            self.render("create_post.html",
                        error="Please enter a subject!",
                        content=content)
        elif not content:
            self.render("create_post.html",
                        error="Please enter some content!",
                        subject=subject)
        else:
            post = BlogPost(subject=subject,
                            content=content,
                            user_id=self.user.key().id(),
                            parent=BLOG_KEY)
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))
