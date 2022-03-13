release: python manage.py migrate
web: NEW_RELIC_CONFIG_FILE=newrelic.ini newrelic-admin run-program gunicorn playlist_connect_project.wsgi --log-file -
worker: python manage.py qcluster