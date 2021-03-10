release: python manage.py migrate

web: gunicorn backend.wsgi --log-file -

worker: python manage.py rqworker high default low email system calls guestUsers activities events
scheduler: python manage.py rqscheduler -i 1
