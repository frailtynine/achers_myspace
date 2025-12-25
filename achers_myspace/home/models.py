from wagtail.models import Page
from wagtail.fields import RichTextField


class HomePage(Page):
    body = RichTextField()

    content_panels = Page.content_panels + [
        "body",
    ]

    def get_context(self, request):
        context = super().get_context(request)

        # Get blog entries
        posts = self.get_children().live().specific()

        # Filter by tag
        tag = request.GET.get('tag')
        if tag:
            posts = posts.filter(blogpage__tagged_items__tag__name=tag)
        context['posts'] = posts
        return context
