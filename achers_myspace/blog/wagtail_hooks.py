from wagtail import hooks
from wagtail.admin.menu import MenuItem
from wagtail.models import Page
from django.urls import reverse

from blog.models import BlogPage


@hooks.register("after_publish_page")
def send_newsletter_on_publish(request, page) -> bool:
    """Send newsletter when a blog post is published."""
    if isinstance(page, BlogPage) and page.send_email:
        if page.send_newsletter():
            BlogPage.objects.filter(pk=page.pk).update(send_email=False)


@hooks.register('register_admin_menu_item')
def register_blog_post_menu_item():
    """Add a quick 'Add Blog Post' button to the admin menu."""
    # Get the HomePage instance
    try:
        homepage = Page.objects.type(Page).filter(depth=2).first()
        if homepage:
            return MenuItem(
                'New Blog Post', 
                reverse('wagtailadmin_pages:add', args=['blog', 'blogpage', homepage.id]),
                icon_name='doc-empty-inverse',
                order=200
            )
    except:
        pass
    return None
