#!/bin/sh
set -e

echo "Waiting for PostgreSQL..."
while ! python src/manage.py check --database default >/dev/null 2>&1; do
  sleep 1
done
echo "PostgreSQL is up."

cd /app/src

python manage.py makemigrations --noinput

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Loading initial exchange rates..."
python manage.py shell -c "from apps.rates.infrastructure.tasks import update_exchange_rates; update_exchange_rates()" || true

echo "Collecting static files..."
python manage.py collectstatic --noinput --clear

echo "Starting Gunicorn..."
exec gunicorn config.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile -