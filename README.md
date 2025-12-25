# Achers MySpace

A Wagtail CMS website for the indie rock band Achers, styled with an old-school MySpace aesthetic featuring dark indie rock themes.

## Features

- **Custom Blog System**: Rich text blog posts with tag support
- **Tag Filtering**: Browse blog posts by tags (music, media, etc.)
- **Email Newsletter**: MailerLite integration for optional sending newsletters when blog posts are published
- **Embed Conversion**: Automatically converts YouTube and Spotify embeds to email-friendly formats (thumbnails and links)
- **MySpace-Inspired UI**: Dark theme (#1a1a1a background, #ff6b6b accents) with gradient headers and bordered modules, two columns and a music player, just like in good old days. 
- **Mobile Responsive**: Optimized layout for desktop and mobile devices

## Tech Stack

- **Backend**: Django 5.2+ with Wagtail 7.2+
- **Database**: PostgreSQL (production), SQLite (development)
- **Package Manager**: uv
- **Email**: MailerLite API
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

# MailerLite
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

# MailerLite
ACHERS_MAILER_API_KEY=your-production-api-key
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

## Email Newsletter (Optional)

Email newsletter functionality is available but optional. When enabled, blog posts can automatically send newsletters via MailerLite when published. The system:
- Converts YouTube embeds to clickable thumbnails
- Converts Spotify embeds to styled links
- Uses email-safe HTML with inline styles
- Schedules campaigns for instant delivery

To disable email newsletters, simply don't configure the `ACHERS_MAILER_API_KEY` environment variable.

## Usage & License

This project is open source and free to use. Feel free to copy, modify, and adapt it for your own band or personal website. No attribution required, though it's appreciated!

**License**: MIT
