release: python manage.py migrate
web: gunicorn playlist_connect_project.wsgi --log-file -
web: python manage.py qcluster