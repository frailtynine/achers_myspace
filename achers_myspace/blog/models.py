import logging

from django.db import models
from django.template.loader import render_to_string

from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from modelcluster.fields import ParentalKey
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TagBase, ItemBase


from blog.email import send_blog_post


logger = logging.getLogger(__name__)


@register_snippet
class BlogTag(TagBase):
    """A tag model for BlogPage instances."""
    free_tagging = False

    class Meta:
        verbose_name = "blog tag"
        verbose_name_plural = "blog tags"


class BlogPageTag(ItemBase):
    """A through model for tagging BlogPage instances."""
    content_object = ParentalKey(
        "BlogPage",
        related_name="tagged_items",
        on_delete=models.CASCADE,
    )
    tag = models.ForeignKey(
        BlogTag,
        related_name="tagged_blogs",
        on_delete=models.CASCADE,
    )


class BlogPage(Page):
    """A Wagtail Page model representing an individual blog post."""
    date = models.DateField("Post date")
    body = RichTextField(blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    send_email = models.BooleanField("Send e-mail", default=False)
    top = models.BooleanField("Pin to top", default=False)

    # Only allow BlogPage as child of HomePage
    parent_page_types = ['home.HomePage']

    # BlogPage cannot have children
    subpage_types = []

    content_panels = Page.content_panels + [
        FieldPanel("date"),
        FieldPanel("body"),
        FieldPanel("tags"),
        FieldPanel("send_email"),
        FieldPanel("top"),
    ]

    def send_newsletter(self) -> bool:
        """Sends an email notification about the blog post."""
        try:
            subject = f"{self.title}"
            html_content = render_to_string("blog/email.html", {
                "page": self,
            })
            send_blog_post(subject, html_content)
            logger.info(f"Sent blog post email for '{self.title}'")
            return True
        except Exception as e:
            logger.error(f"Error sending blog post email: {e}", exc_info=True)
            import traceback
            logger.error(traceback.format_exc())
            return False
