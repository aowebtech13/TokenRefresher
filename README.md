# Axiom Token Refresher

A Django-based utility to automatically and manually refresh Axiom tokens, designed for deployment on AWS.

## Features
- **Dashboard**: Monitor token status and recent refresh history.
- **Manual Refresh**: Trigger an immediate token refresh via the UI.
- **Automated Refresh**: Management command `refresh_tokens` for scheduling via Cron or AWS Lambda.
- **Database Logging**: Keeps a history of all refresh attempts (success/failure).
- **Production Ready**: Optimized with WhiteNoise for static files and environment-based configuration.

## Setup Instructions

### 1. Prerequisites
- Python 3.9+
- Pip

### 2. Installation
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate
```

### 3. Configuration
Create a `.env` file in the root directory (see `.env.example`):
- `AXIOM_REFRESH_URL`: The Axiom API endpoint.
- `AXIOM_REFRESH_TOKEN`: Your persistent refresh token.
- `TOKENS_FILE`: Path where the new access token will be written (default: `TOKENS.txt`).
- `DJANGO_SECRET_KEY`: A secure key for production.
- `DEBUG`: Set to `False` in production.
- `ALLOWED_HOSTS`: Comma-separated list of domains (e.g., `your-app.aws-region.elb.amazonaws.com`).

### 4. Running Locally
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000` to see the dashboard.

## Management Command
To automate the refresh, schedule this command using a cron job or task scheduler:
```bash
python manage.py refresh_tokens
```

## AWS Deployment Tips

### Static Files
The project is configured with **WhiteNoise**. Run the following before deploying:
```bash
python manage.py collectstatic
```

### Database
By default, this uses `sqlite3`. For highly available AWS deployments, consider switching the `DATABASES` setting in `settings.py` to use **Amazon RDS (PostgreSQL/MySQL)**.

### Application Server
Use **Gunicorn** (included in `requirements.txt`) to serve the application:
```bash
gunicorn token_refresher.wsgi:application --bind 0.0.0.0:8000
```

### Scheduling
On an EC2 instance, you can add a crontab entry to refresh every hour:
```bash
0 * * * * cd /path/to/app && /path/to/venv/bin/python manage.py refresh_tokens >> /var/log/token_refresh.log 2>&1
```
