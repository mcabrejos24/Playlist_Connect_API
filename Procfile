release: python manage.py migrate
web: gunicorn playlist_connect_project.wsgi --log-file -
worker: python manage.py qcluster --settings=path.to.my.settings