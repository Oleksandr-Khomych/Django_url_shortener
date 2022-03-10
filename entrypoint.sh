bash -c "sleep 5s"

python manage.py migrate

python manage.py collectstatic --noinput

gunicorn Django_url_shortener.wsgi:application --bind 0.0.0.0:8000
