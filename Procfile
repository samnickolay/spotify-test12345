release: python manage.py makemigrations
release: python manage.py migrate --run-syncdb
release: python manage.py migrate

web: gunicorn backend.wsgi --log-file -


