import re
from urllib.parse import urljoin
import logging

import mailerlite
from bs4 import BeautifulSoup

from achers_myspace.settings.base import MAILER_API_KEY

logger = logging.getLogger(__name__)

SPOTIFY_EMBED_REGEX = r'spotify\.com/embed/(playlist|album|track)/([^?]+)'


def convert_embeds_for_email(
    html_content: str,
    base_url: str = "https://achers.org",
) -> str:
    """Convert YouTube and Spotify embeds to email-friendly format."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Convert all relative image URLs to absolute
    for img in soup.find_all('img'):
        src = img.get('src', '')
        if src and not src.startswith(('http://', 'https://', 'data:')):
            # Convert relative URL to absolute
            img['src'] = urljoin(base_url, src)

    # Find all iframes (YouTube and Spotify embeds)
    for iframe in soup.find_all('iframe'):
        src = iframe.get('src', '')

        # YouTube embeds
        if 'youtube.com' in src or 'youtu.be' in src:
            # Extract video ID from iframe src
            match = re.search(r'embed/([^?]+)', src)
            if match:
                video_id = match.group(1)
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                thumbnail_url = (
                    f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"
                )

                # Create email-friendly replacement
                replacement = soup.new_tag(
                    'div', style='margin: 20px 0; text-align: center;'
                )
                link = soup.new_tag(
                    'a', href=video_url, style='display: block;'
                )
                img = soup.new_tag(
                    'img',
                    src=thumbnail_url,
                    alt='Watch on YouTube',
                    style=(
                        'max-width: 100%; height: auto; '
                        'border: 2px solid #333;'
                    )
                )
                link.append(img)
                replacement.append(link)
                iframe.replace_with(replacement)

        # Spotify embeds
        elif 'spotify.com' in src:
            # Extract Spotify URL
            match = re.search(
                SPOTIFY_EMBED_REGEX, src
            )
            if match:
                content_type = match.group(1)
                content_id = match.group(2)
                title = iframe.get('title', 'Listen on Spotify')
                if title != "Listen on Spotify":
                    title = title.replace('Spotify Embed: ', '')
                spotify_url = (
                    f"https://open.spotify.com/{content_type}/{content_id}"
                )
                # Create email-friendly replacement
                div_style = (
                    "margin: 20px 0; padding: 15px; background: #222; "
                    "border: 2px solid #333; text-align: center;"
                )
                replacement = soup.new_tag('div', style=div_style)
                text_p = soup.new_tag('p', style='margin: 0;')
                link = soup.new_tag(
                    'a', href=spotify_url,
                    style=(
                        'color: #ff6b6b; font-weight: bold; '
                        'text-decoration: none;'
                    )
                )
                link.string = title
                text_p.append(link)
                replacement.append(text_p)
                iframe.replace_with(replacement)
    return str(soup)


def send_blog_post(
    subject: str,
    content: str,
):
    """Sends an email with the given body using MailerLite."""
    # Convert embeds to email-friendly format
    email_content = convert_embeds_for_email(content)

    mailer = mailerlite.Client({
        "api_key": MAILER_API_KEY
    })

    params = {
        "name": subject,
        "language_id": 1,
        "type": "regular",
        "emails": [{
            "subject": subject,
            "from_name": "Achers",
            "from": "achers@achers.org",
            "content": email_content
        }]
    }

    response = mailer.campaigns.create(params)
    campaign_id = int(response['data']['id'])
    mailer.campaigns.schedule(campaign_id, {"delivery": "instant"})
