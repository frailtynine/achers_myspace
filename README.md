# Achers MySpace

A Wagtail CMS website for a rock band, styled with an old-school MySpace, with newsletter integration.

The project is tailored for London indie rock band [Achers](https://achers.org), but with few adjustments can be used anywhere. 

## Features

- **Custom Blog System**: Rich text blog posts with tag support
- **Tag Filtering**: Browse blog posts by tags (music, media, gigs, etc.)
- **Newsletter Integration**: Support for both Mailchimp (embedded signup form) and MailerLite (popup form)
- **Email Newsletter**: Newsletter integration (supports Mailchimp and Mailerlite)
- **Embed Conversion**: Automatically converts YouTube and Spotify embeds to email-friendly formats (thumbnails and links)
- **MySpace-Inspired UI**: Dark theme (#1a1a1a background, #ff6b6b accents) with gradient headers and bordered modules, two columns and a music player, just like in good old days. 
- **Mobile Responsive**: Optimized layout for desktop and mobile devices

## Tech Stack

- **Backend**: Django 5.2+ with Wagtail 7.2+
- **Database**: PostgreSQL (production), SQLite (development)
- **Package Manager**: uv
- **Newsletter**: Mailchimp or MailerLite
- **Deployment**: Docker with Nginx reverse proxy
- **Frontend**: Wagtail templates with MySpace aesthetic

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL (for production)
- Docker & Docker Compose (for deployment)

## Local Development

### Setup

1. Clone the repository:
```bash
git clone https://github.com/frailtynine/achers_myspace.git
cd achers_myspace
```

2. Install dependencies:
```bash
make install
```

3. Set up environment variables (create `.env` in project root):
```env
# Development settings
ACHERS_SECRET_KEY=your-secret-key-here
ACHERS_DEBUG=True
ACHERS_ALLOWED_HOSTS=localhost,127.0.0.1

# Database (SQLite for dev - no DATABASE_URL needed)
# For PostgreSQL: ACHERS_DATABASE_URL=postgres://user:pass@localhost:5432/dbname

# Newsletter Integration (choose one)
# Mailchimp - for embedded signup form and wagtail-newsletter integration
WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY=your-mailchimp-api-key

# MailerLite - for popup form and programmatic email sending
ACHERS_MAILER_API_KEY=your-mailerlite-api-key
```

4. Run migrations:
```bash
make migrate
```

5. Create a superuser:
```bash
make superuser
```

6. Run development server:
```bash
make run
```

Visit http://127.0.0.1:8000 to see the site and http://127.0.0.1:8000/admin to access the Wagtail admin.

### Available Make Commands

```bash
make install        # Install dependencies with uv
make sync           # Sync dependencies from lock file
make migrate        # Run database migrations
make makemigrations # Create new migrations
make run            # Run development server
make superuser      # Create a superuser
make shell          # Start Django shell
make test           # Run tests
make check          # Check for project issues
make collectstatic  # Collect static files
make clean          # Remove Python cache files
make startapp       # Create new app (make startapp name=appname)
```

## Docker Deployment

### Production Setup

1. Configure environment variables in `.env`:
```env
# Django settings
ACHERS_SECRET_KEY=your-production-secret-key
ACHERS_DEBUG=False
ACHERS_ALLOWED_HOSTS=achers.org,www.achers.org

# PostgreSQL
ACHERS_POSTGRES_DB=achers_db
ACHERS_POSTGRES_USER=achers
ACHERS_POSTGRES_PASSWORD=strong-password
ACHERS_DATABASE_URL=postgres://achers:strong-password@db:5432/achers_db

# Newsletter Integration
WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY=your-mailchimp-api-key
ACHERS_MAILER_API_KEY=your-mailerlite-api-key  # Optional
```

2. Build and run with Docker Compose:
```bash
docker compose up --build
```

3. Create superuser (in another terminal):
```bash
docker compose exec web python manage.py createsuperuser
```

The site will be available at http://localhost:80

### Docker Services

- **db**: PostgreSQL 15 database
- **migrate**: Runs database migrations before starting web server
- **web**: Gunicorn application server
- **nginx**: Reverse proxy serving static files and routing requests

## Project Structure

```
achers/
├── achers_myspace/          # Django project
│   ├── achers_myspace/      # Settings and config
│   │   ├── settings/        # Split settings (base, dev, production)
│   │   ├── static/          # Main CSS and JS
│   │   └── templates/       # Base templates
│   ├── blog/                # Blog app with rich text
│   │   ├── models.py        # BlogPage model with tags
│   │   ├── email.py         # MailerLite integration (optional)
│   │   └── templates/       # Blog templates
│   ├── home/                # Homepage app
│   │   ├── models.py        # HomePage with tag filtering
│   │   └── templates/       # Home page templates
│   └── search/              # Search functionality
├── docker-compose.yml       # Docker orchestration
├── nginx.conf               # Nginx configuration
├── Makefile                 # Development commands
└── pyproject.toml           # Python dependencies
```

## Newsletter Integration

The project supports two newsletter integration options that can be used independently or together:

### Option 1: Mailchimp (Default - Recommended)

**Features:**
- Embedded signup form on homepage (styled to match MySpace theme)
- Integration with `wagtail-newsletter` package
- Newsletter sending via Wagtail admin

**Setup:**

1. Get your Mailchimp API key from [Mailchimp Account Settings](https://admin.mailchimp.com/account/api/)

2. Create an embedded signup form in Mailchimp:
   - Go to **Forms** → **Other forms** → **Create embedded form**
   - Choose your audience
   - Copy the generated HTML code

3. Add the signup form HTML to `achers_myspace/home/templates/home/home_page.html` inside the `#mc_embed_shell` div (already present in the template, replace it).

4. Set environment variable:
```env
WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY=your-mailchimp-api-key
```

5. The CSS styling is already configured in `static/css/achers_myspace.css` to match the MySpace theme

**To disable Mailchimp:**

Mailchimp integration uses the `wagtail-newsletter` package via `NewsletterPageMixin` which adds database fields and admin panels to BlogPage. To fully disable it:

1. Remove or comment out the `#mc_embed_shell` section from `home_page.html`
2. Remove the `WAGTAIL_NEWSLETTER_MAILCHIMP_API_KEY` from `.env`
3. **Note**: Mailchimp-related fields will still appear in Wagtail admin (newsletter campaign, recipients, subject) due to the `NewsletterPageMixin`. To completely remove these:
   - Remove `NewsletterPageMixin` from `BlogPage` class in `blog/models.py`
   - Remove `from wagtail_newsletter.models import NewsletterPageMixin` import
   - Run `python manage.py makemigrations` and `python manage.py migrate`
   - This will remove the newsletter fields from the database

### Option 2: MailerLite (Alternative)

**Features:**
- Popup signup form (triggered by button click or automatically)
- Programmatic email sending via API
- Lighter weight integration
- Manual control over when popup appears
- Uses custom `send_email` field (already in database, hidden by default)

**Setup:**

1. Get your MailerLite API key from [MailerLite Settings](https://dashboard.mailerlite.com/integrations/api)

2. Get your popup form ID:
   - Create a popup form in MailerLite dashboard
   - Copy the form ID (e.g., `QY0gfK`)

3. Uncomment the MailerLite Universal script in `achers_myspace/achers_myspace/templates/base.html`:
```html
<!-- MailerLite Universal -->
<script>
    (function(w,d,e,u,f,l,n){w[f]=w[f]||function(){(w[f].q=w[f].q||[])
    .push(arguments);},l=d.createElement(e),l.async=1,l.src=u,
    n=d.getElementsByTagName(e)[0],n.parentNode.insertBefore(l,n);})
    (window,document,'script','https://assets.mailerlite.com/js/universal.js','ml');
    ml('account', 'YOUR_ACCOUNT_ID');
</script>
<!-- End MailerLite Universal -->
```

4. Add a trigger button in `home_page.html` (replace the Mailchimp form):
```html
<button class="ml-onclick-form" onclick="ml('show', 'YOUR_FORM_ID', true)">
    Subscribe to Newsletter
</button>
```

5. Set environment variable:
```env
ACHERS_MAILER_API_KEY=your-mailerlite-api-key
```

6. **Enable the "Send e-mail" field in admin** (currently hidden):
   - In `blog/models.py`, add `FieldPanel("send_email")` to `content_panels` list
   - This checkbox enables automatic newsletter sending via MailerLite API when publishing blog posts

**To disable MailerLite:**
- Comment out the MailerLite script in `base.html` (currently commented out by default)
- Remove the popup trigger button from `home_page.html`
- Remove the `ACHERS_MAILER_API_KEY` from `.env`

### Email Sending on Blog Post Publish

When blog posts are published with the "Send e-mail" checkbox enabled, the system can automatically send newsletters. This functionality uses MailerLite API (`blog/email.py`) and includes:
- Automatic conversion of YouTube embeds to clickable thumbnails
- Conversion of Spotify embeds to styled links
- Email-safe HTML with inline styles
- Instant campaign delivery

**Note:** This feature requires `ACHERS_MAILER_API_KEY` to be configured.

## Usage & License

This project is open source and free to use. Feel free to copy, modify, and adapt it for your own band or personal website. No attribution required, though it's appreciated!

**License**: MIT
