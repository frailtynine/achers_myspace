from wagtail import hooks

from blog.models import BlogPage


@hooks.register("after_publish_page")
def send_newsletter_on_publish(request, page) -> bool:
    """Send newsletter when a blog post is published."""
    if isinstance(page, BlogPage) and page.send_email:
        if page.send_newsletter():
            BlogPage.objects.filter(pk=page.pk).update(send_email=False)
