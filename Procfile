release: python manage.py migrate
web: newrelic-admin run-program gunicorn playlist_connect_project.wsgi --log-file -
worker: python manage.py qcluster