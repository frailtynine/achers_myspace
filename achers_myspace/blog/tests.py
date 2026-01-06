# ===================================================================
# COMMENTED OUT: MailerLite integration tests (replaced with wagtail-newsletter)
# ===================================================================
# from unittest.mock import patch, MagicMock
# 
# from django.test import TestCase
# 
# from blog.email import convert_embeds_for_email, send_blog_post
# 
# 
# class ConvertEmbedsForEmailTest(TestCase):
#     """Tests for the convert_embeds_for_email function."""
# 
#     def test_converts_relative_image_urls_to_absolute(self):
#         html = '<img src="/media/images/photo.jpg">'
#         result = convert_embeds_for_email(html)
#         self.assertIn('src="https://achers.org/media/images/photo.jpg"', result)
# 
#     def test_preserves_absolute_image_urls(self):
#         html = '<img src="https://example.com/image.jpg">'
#         result = convert_embeds_for_email(html)
#         self.assertIn('src="https://example.com/image.jpg"', result)
# 
#     def test_preserves_data_urls(self):
#         html = '<img src="data:image/png;base64,abc123">'
#         result = convert_embeds_for_email(html)
#         self.assertIn('src="data:image/png;base64,abc123"', result)
# 
#     def test_custom_base_url(self):
#         html = '<img src="/images/test.png">'
#         result = convert_embeds_for_email(html, base_url="https://custom.com")
#         self.assertIn('src="https://custom.com/images/test.png"', result)
# 
#     def test_converts_youtube_embed_to_thumbnail_link(self):
#         html = '<iframe src="https://www.youtube.com/embed/dQw4w9WgXcQ"></iframe>'
#         result = convert_embeds_for_email(html)
# 
#         self.assertNotIn('<iframe', result)
#         self.assertIn('href="https://www.youtube.com/watch?v=dQw4w9WgXcQ"', result)
#         self.assertIn(
#             'src="https://img.youtube.com/vi/dQw4w9WgXcQ/maxresdefault.jpg"',
#             result
#         )
#         self.assertIn('alt="Watch on YouTube"', result)
# 
#     def test_converts_youtube_embed_with_query_params(self):
#         html = '<iframe src="https://www.youtube.com/embed/abc123?autoplay=1"></iframe>'
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('href="https://www.youtube.com/watch?v=abc123"', result)
# 
#     def test_converts_spotify_playlist_embed(self):
#         html = (
#             '<iframe src="https://open.spotify.com/embed/playlist/123abc" '
#             'title="Spotify Embed: My Playlist"></iframe>'
#         )
#         result = convert_embeds_for_email(html)
# 
#         self.assertNotIn('<iframe', result)
#         self.assertIn('href="https://open.spotify.com/playlist/123abc"', result)
#         self.assertIn('My Playlist', result)
# 
#     def test_converts_spotify_album_embed(self):
#         html = (
#             '<iframe src="https://open.spotify.com/embed/album/456def" '
#             'title="Spotify Embed: Cool Album"></iframe>'
#         )
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('href="https://open.spotify.com/album/456def"', result)
#         self.assertIn('Cool Album', result)
# 
#     def test_converts_spotify_track_embed(self):
#         html = (
#             '<iframe src="https://open.spotify.com/embed/track/789ghi" '
#             'title="Spotify Embed: Song Name"></iframe>'
#         )
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('href="https://open.spotify.com/track/789ghi"', result)
#         self.assertIn('Song Name', result)
# 
#     def test_spotify_embed_default_title(self):
#         html = '<iframe src="https://open.spotify.com/embed/track/abc"></iframe>'
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('Listen on Spotify', result)
# 
#     def test_preserves_non_embed_iframes(self):
#         html = '<iframe src="https://example.com/widget"></iframe>'
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('<iframe', result)
#         self.assertIn('src="https://example.com/widget"', result)
# 
#     def test_handles_multiple_embeds(self):
#         html = '''
#         <iframe src="https://www.youtube.com/embed/video1"></iframe>
#         <iframe src="https://open.spotify.com/embed/track/track1"></iframe>
#         <iframe src="https://www.youtube.com/embed/video2"></iframe>
#         '''
#         result = convert_embeds_for_email(html)
# 
#         self.assertNotIn('<iframe', result)
#         self.assertIn('watch?v=video1', result)
#         self.assertIn('watch?v=video2', result)
#         self.assertIn('open.spotify.com/track/track1', result)
# 
#     def test_handles_mixed_content(self):
#         html = '''
#         <p>Check out this video:</p>
#         <iframe src="https://www.youtube.com/embed/xyz"></iframe>
#         <img src="/media/photo.jpg">
#         <p>And this song:</p>
#         <iframe src="https://open.spotify.com/embed/track/abc"></iframe>
#         '''
#         result = convert_embeds_for_email(html)
# 
#         self.assertIn('<p>Check out this video:</p>', result)
#         self.assertIn('<p>And this song:</p>', result)
#         self.assertIn('https://achers.org/media/photo.jpg', result)
#         self.assertNotIn('<iframe', result)
# 
#     def test_empty_html(self):
#         result = convert_embeds_for_email('')
#         self.assertEqual(result, '')
# 
#     def test_html_without_embeds_or_images(self):
#         html = '<p>Just some text</p>'
#         result = convert_embeds_for_email(html)
#         self.assertIn('<p>Just some text</p>', result)
# 
# 
# class SendBlogPostTest(TestCase):
#     """Tests for the send_blog_post function."""
# 
#     @patch('blog.email.mailerlite.Client')
#     def test_creates_and_schedules_campaign(self, mock_client_class):
#         mock_client = MagicMock()
#         mock_client_class.return_value = mock_client
#         mock_client.campaigns.create.return_value = {
#             'data': {'id': '12345'}
#         }
# 
#         send_blog_post('Test Subject', '<p>Test content</p>')
# 
#         mock_client.campaigns.create.assert_called_once()
#         call_args = mock_client.campaigns.create.call_args[0][0]
#         self.assertEqual(call_args['name'], 'Test Subject')
#         self.assertEqual(call_args['emails'][0]['subject'], 'Test Subject')
#         self.assertEqual(call_args['emails'][0]['from_name'], 'Achers')
#         self.assertEqual(call_args['emails'][0]['from'], 'achers@achers.org')
# 
#         mock_client.campaigns.schedule.assert_called_once_with(
#             12345, {"delivery": "instant"}
#         )
# 
#     @patch('blog.email.mailerlite.Client')
#     def test_converts_embeds_before_sending(self, mock_client_class):
#         mock_client = MagicMock()
#         mock_client_class.return_value = mock_client
#         mock_client.campaigns.create.return_value = {
#             'data': {'id': '1'}
#         }
# 
#         html_with_embed = '<iframe src="https://www.youtube.com/embed/test"></iframe>'
#         send_blog_post('Subject', html_with_embed)
# 
#         call_args = mock_client.campaigns.create.call_args[0][0]
#         content = call_args['emails'][0]['content']
#         self.assertNotIn('<iframe', content)
#         self.assertIn('youtube.com/watch?v=test', content)
# ===================================================================


# ===================================================================
# NEW: Mailchimp integration tests (via wagtail-newsletter)
# ===================================================================
from django.test import TestCase
from django.utils import timezone

from wagtail.models import Page
from home.models import HomePage

from blog.models import BlogPage


class BlogPageNewsletterIntegrationTest(TestCase):
    """Tests for BlogPage integration with wagtail-newsletter."""

    def setUp(self):
        """Set up test data."""
        # Get the root page
        root = Page.objects.get(id=1)
        
        # Create a HomePage as parent with a unique slug
        self.home_page = HomePage(
            title="Test Home",
            slug="test-home",
            body="Test home page",
        )
        root.add_child(instance=self.home_page)
        self.home_page.save_revision().publish()

    def test_blog_page_has_newsletter_fields(self):
        """Test that BlogPage has newsletter-related fields from NewsletterPageMixin."""
        blog_page = BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
            date=timezone.now().date(),
            body="Test content",
        )
        
        # Check that newsletter fields are available
        self.assertTrue(hasattr(blog_page, 'newsletter_recipients'))
        self.assertTrue(hasattr(blog_page, 'newsletter_subject'))
        self.assertTrue(hasattr(blog_page, 'newsletter_campaign'))

    def test_blog_page_newsletter_template_configured(self):
        """Test that BlogPage has the correct newsletter template."""
        blog_page = BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
            date=timezone.now().date(),
            body="Test content",
        )
        
        self.assertEqual(blog_page.newsletter_template, "blog/email.html")

    def test_get_newsletter_subject_defaults_to_title(self):
        """Test that newsletter subject defaults to page title."""
        blog_page = BlogPage(
            title="My Blog Post Title",
            slug="my-blog-post",
            date=timezone.now().date(),
            body="Test content",
        )
        
        # When newsletter_subject is not set, it should return the title
        self.assertEqual(blog_page.get_newsletter_subject(), "My Blog Post Title")

    def test_get_newsletter_subject_custom(self):
        """Test that custom newsletter subject is used when provided."""
        blog_page = BlogPage(
            title="My Blog Post Title",
            slug="my-blog-post",
            date=timezone.now().date(),
            body="Test content",
            newsletter_subject="Custom Newsletter Subject",
        )
        
        self.assertEqual(blog_page.get_newsletter_subject(), "Custom Newsletter Subject")

    def test_get_newsletter_context(self):
        """Test that newsletter context includes the page."""
        blog_page = BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
            date=timezone.now().date(),
            body="Test content",
        )
        
        context = blog_page.get_newsletter_context()
        self.assertIn('page', context)
        self.assertEqual(context['page'], blog_page)

    def test_get_newsletter_html(self):
        """Test that newsletter HTML is generated from template."""
        self.home_page.add_child(instance=BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
            date=timezone.now().date(),
            body="<p>Test content</p>",
        ))
        blog_page = BlogPage.objects.get(slug="test-blog-post")
        
        html = blog_page.get_newsletter_html()
        
        # Check that the HTML contains expected elements from the template
        self.assertIn("Test Blog Post", html)
        self.assertIn("Test content", html)
        
    def test_send_email_field_exists(self):
        """Test that send_email field still exists for backward compatibility."""
        blog_page = BlogPage(
            title="Test Blog Post",
            slug="test-blog-post",
            date=timezone.now().date(),
            body="Test content",
            send_email=True,
        )
        
        self.assertTrue(blog_page.send_email)
