# Music Connect API

Code for the backend of the Music Connect Project


To spin up development server:
- vagrant up (wait for it to finish running)
- vagrant ssh (to connect to the vagrant server on virtual box)
- cd /vagrant (to move into the directory that is synced up with our local machine project directory)
- python -m venv ~/env (to create a python virtual env so it won't affect your local machine | important incase you need to respin up the vagrant server)
    - "~/" is specified so the virtual environment is created on the home directory of the vagrant folder as opposed to the local directory of our computer
    - this only needs be run once when creating the virtual environment
- source ~/env/bin/activate (to activate the python virtual environment)
    - deactive (when you want to deactivate the python virtual environment)
- pip install -r requirements.txt (to install the packages in the requirements.txt file)
- python manage.py runserver 0.0.0.0:8000
    - '0.0.0.0' makes the server accessible on all network adapters on our server
    - ':8000' is for port 8000
    - ctrl-c (stops the server)





# When creating project

- django-admin.py startproject playlist_connect_project .
- python manage.py startapp playlist_connect_api
- enable new app in settings.py in playlist_connect_project
    - add 'rest_framework' to INSTALLED_APPS
    - add 'rest_framework.authtoken'
    - add {new_app_name}
    - add trailing comma ',' at the end of each line