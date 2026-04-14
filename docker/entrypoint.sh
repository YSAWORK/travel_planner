#!/bin/sh
# Path: docker/entrypoint.sh
# Entrypoint script for Django application
set -e

# Load environment variables from .env file if it exists
echo "Applying database migrations..."
python manage.py migrate --noinput || { echo "Migration failed!"; exit 1; }

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput || { echo "Collectstatic failed!"; exit 1; }

# Create superuser if environment variables are set
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_EMAIL" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
  echo "Ensuring superuser exists..."
  python manage.py shell -c "
from django.contrib.auth import get_user_model;
User = get_user_model();
if not User.objects.filter(username='${DJANGO_SUPERUSER_USERNAME}').exists():
    User.objects.create_superuser('${DJANGO_SUPERUSER_USERNAME}', '${DJANGO_SUPERUSER_EMAIL}', '${DJANGO_SUPERUSER_PASSWORD}');
" || echo "WARNING: Superuser creation failed!"
fi

# Start Gunicorn server
echo "Starting Gunicorn on port ${PORT:-8000}..."
exec gunicorn --workers 3 --bind 0.0.0.0:${PORT:-8000} travel_service.wsgi:application
