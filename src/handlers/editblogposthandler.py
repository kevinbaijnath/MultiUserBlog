from ..constants import BLOG_KEY
from ..handlers.bloghandler import BlogHandler
from ..helpers.decorators import (logged_in,
                                  blogpost_exists,
                                  user_authorized_blogpost)
from ..models.blogpost import BlogPost


class EditBlogPostHandler(BlogHandler):
    """Defines the edit blog functionality"""

    @logged_in
    @blogpost_exists
    @user_authorized_blogpost
    def get(self, blog_id):
        """Shows the user the edit blog page"""
        blog_post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)
        self.render("create_post.html",
                    content=blog_post.content,
                    subject=blog_post.subject,
                    blog_id=blog_id)

    @logged_in
    @blogpost_exists
    @user_authorized_blogpost
    def post(self, blog_id):
        """Updates the post"""
        post = BlogPost.get_by_id(int(blog_id), parent=BLOG_KEY)

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
            post.subject = subject
            post.content = content
            post.put()
            self.redirect('/blog/{0}'.format(str(post.key().id())))
