# Playlist Pair API

Playlist Pair is a project I wanted to do to solve the problem of people not being able to share playlists when they have different music services. Now, with this project, users are able to sync up their gym, work, etc. type of playlists with their friends that use another platform.

An alternative way of using the project is for when you are switching services yourself. If you decide to go from Spotify to Apple, or vice-versa, then you can use this project to move each of your playlists with ease.

Playlist Pair is accessible at [playlistpair.com]

The frontend of the project is accessible at [Playlist Pair Frontend].

## Getting Started

This project uses [git], [vagrant] and [virtualbox]. Make sure these are all downloaded for your appropriate machine before continuing.

Note: vagrant and virtualbox are just used for local development.

To start using vagrant, navigate to the project root directory. Once there, run:
```
vagrant up
```
This will spin up a vagrant server instance on your virtualbox. Then, run:
```
vagrant ssh
```
Which will then connect you to the vagrant server. After, run:
```
cd /vagrant
```
This will move you into a vagrant directory that is in sync with the project root directory on your local machine. If you run:
```
ls
```
you will see the same files in your root project directory, thus, any updates to files in here will update the files in your root directory. If you want to exit the vagrant instance and return to your computer's regular terminal, then run:
```
exit
```
and you should return. Once you have entered the vagrant directory, run:
```
python -m venv ~/env
```
to create a virtual enviornment so it won't affect your local machine (this is important in the case that you need to respin up the vagrant server). "~/" is specified so the virtual environment is created on the home directory of the vagrant folder as opposed to the local directory of our computer. This only needs to run once when creating the virtual environment. Following that run:
```
source ~/env/bin/activate
```
to activate the python virtual environment you just created. To exit from your virtual environment at any time, run:
```
deactivate
```
Each time you exit and stop working on your project, run the first set up commands at the top of the "Running the website locally" section. You do not need to run all of the commands in this section again, only when you are getting started.

Next we want to make sure we install all of our project dependencies in our requirements.txt file. Run:
```
pip install -r requirements.txt
```
Once this has been done, your project is ready to run.


## Running the website locally

If you are coming from the "Getting Started" section above, you can skip this step and move on to the next. If not, then to make sure you are back on the vagrant server and in your virtual environment, run:
```
vagrant up (only if vagrant ssh states that your server has been shut down)
vagrant ssh
cd /vagrant
source ~/env/bin/activate
```
and you will be good to go.

Before we run our project we need to do two things. First, make sure to navigate to the 'settings.py' file in the 'playlist_connect_project' directory and change the line that says:
```
DEBUG = False
```
to 'True'.

Second, you will need to add a '.env' file to the project root directory with specific environment variables. To access these variables, reach out to the project administrator.

Then you're ready to run the project locally.

To run our project locally, run:
```
python manage.py runserver 0.0.0.0:8000
```
Append this with command with '--noreload' if your terminal seems to endlessly refresh the server instance. Looks like:
```
python manage.py runserver 0.0.0.0:8000 --noreload
```
The '0.0.0.0' in the command makes the server accessible on all network adapters on our server. The ':8000' run it on port 8000. To stop the server, PRESS:
```
ctrl-c 
```
After this, your project should be running and you can visit it by going to 'localhost:8000' or '127.0.0.1:8000'. When you go to the path, you will notice that there seems to be an error. This is because there is now view setup for this path. To view your API, append the '/api' path to your url.

So head to 'localhost:8000/api' and you will see an API view. Here there will be a link to 'localhost:8000/api/playlistpairs' path which contain your model instances in the database. However, nothing will be shown yet because first need to migrate your models to the database.

Follow the next section to migrate your models.

## Migrate models

To migrate your django models, run:
```
python manage.py makemigrations
```
so that any updates or additions to models are made. If there are any, you will see them under 'playlist_connect_api/migrations'. Next, run:
```
python manage.py migrate
```
to apply your migrations to the database. Now when you visit 'localhost:8000/api/playlistpairs' you will see the view to see your model instances. Though, for now you will only see an empty array '[]' until you add instances. Below, you will see a form that will allow you to populate the database. If you eneter data into it, once you click the 'POST' button and refresh the page, you will then see a new model instance.

However, to add real playlistpair instances, you will either need to use the frontend and provide real account playlists or enter the correct data manually. Otherwise the syncing functionalities will not work.

One other thing neccessary to make the syncing functionality work is to add a scheduler which is done via the Django admin. You will also want to remove any instances you might have added when messing around with the form because then the syncing functionality will not work with these instances.

Read the next section to find how to enter the Django admin and update instances/set up a scheduler.

## Scheduling Syncs and accessing the Django Admin to update model instances.

Before being able to access the Django admin, you first need to create a superuser account. To do this run:
```
python manage.py createsuperuser
```
Follow the instructions on your terminal to set up an account. Make sure you do not forget your username and password. In the case that you do though, you can simply run this command again to create another superuser.

Next, in your browser, navigate to 'localhost:8000/admin'. This will bring you to a page where you can enter your superuser username and password. Once you've entered, you will see 4 tabs.

Under the 'AUTH TOKEN' tab, there are instances of tokens that our project uses. Under 'AUTHENTICATION AND AUTHORIZATION' you can add or remove superusers. Under 'DJANGO Q' you can add/remove/update scheduled tasks and view scheduled ones or old ones. Under 'PLAYLIST_CONNECT_API' you can view instances of our models.

The only tabs we care about are the latter 3. To remove a superuser because you maybe forgot its password, go to 'Users' under "AUTHENTICATION AND AUTHORIZATION' and click on a user. Once in there, you can remove one by pressing 'REMOVE' at the bottom of the page.

To erase playlist pair instances, go to 'Playlist pairss' under 'PLAYLIST_CONNECT_API', click on the instance you want to delete, check the data in there to make sure the instances data matches the one you want to delete, and press the 'DELETE' button at the bottom of the page.

Lastly, to set up a scheduler so that our playlists are scheduled to sync up, click that '+Add' button next to the 'Scheduled tasks' button under 'DJANGO Q'. This will take you to a page where you need to input information for a scheduler.

The only things neccessary for us to run a scheduler will be 'Name', 'Func', "Schedule Type', 'Minutes', 'Repeats', and 'Next Run'.

For 'Name', name it anything you like, such as 'Sync All DB Playlists'.

For 'Func', pass in 'playlist_connect_api.schedule.sync_all_playlists', which will point to the 'sync_all_playlists' function in the 'schedule' file' under the 'playlist_connect_api directory in our project.

For 'Schedule Type', enter 'Minutes' so that we can specify in minutes, how often our project should run. Note, if you want to test this project running every hour, day, etc. then change it accordingly.

For 'Minutes', enter '1' or however many minutes you would like the scheduler to run.

For 'Repeats' enter '-1' so that our scheduler runs forever. Note, when revisiting your scheduler instance, you might notice this number might have changed to a number less than '-1' such as '-3000'. This is okay, it just means it has run that many times since entering '-1'.

For 'Next Run', press 'Now' and 'Today' and make sure you know your time zone relative to this by reading the note below that says 'Note: You are X hours [behind/ahead] of server time'.

After all of this info has been entered, press the 'SAVE' button at the bottom to save your scheduler instance.

Once you are done creating your scheduler, you will need to activate it. Open another terminal in your project, making sure you enter the vagrant server, the /vagrant directory, and the python virtual environment (see instructions at the top of "Running the website locally".

Once in, run:
```
python ./manage.py qcluster
```
to run your scheduler.

You will see print statements in this terminal every minute (or however long you chose to run the scheduler) with information on if your model instances were successfully synced.

## Running and Adding Tests
To run tests, run:
```
python manage.py test
```
This will run all of the tests in the project.

To add tests, navigate to the 'tests.py' file under the 'playlist_connect_api' folder.

The 'TestCase' library for Django is used here. Append any tests to the bottom of this file.


## Contributing

If you would like to contribute to this project, branch off from the master branch and name your branches accordingly:
- new features:         feature/<name of feature>
- bug fixes:            fix/<name of fix>
- simple updates:       chore/<name of the update>

Once you make your changes on your new brach, commit and submit a pull request.

Note: DON'T FORGET TO CHANGE
```
DEBUG = True
```
back to 'False'

Tests will run against your changes. If they do not pass, read the log to see why they failed. If they pass then request a review from @mcabrejos24.

Once a review has been submitted and approved, you may merge the pull request.

This project is hosted on [heroku] and can be accessed here at [heroku playlistpair].

Note you will need to have a heroku account and be a memeber of the project on heroku to access it.

Message the project administrator for access.

## Heroku info
If the site is shut down but you want to start it back up, this will have to be done on the heroku dashboard in the project directory. However, to make sure the scheduler is run on live, like it is here in development, you will need to install the [heroku cli] and navigate to your terminal to run:
```
heroku ps:scale worker=1
```
This will start the scheduler, basically running 'python ./manage.py qcluster' but on live since heroku does not automatically run this when starting up the project.

Sometimes there will be logs you will want to see from the live site. To view the logs, run:
```
heroku logs --tail
```
This will allow you to read the logs from the live site to check for errors, processess, etc.


## When creating a django project
Here are just some commands that were run when creating this Django project. It will be a reference for anyone who is curious and wants to create a Django project or another application within this Django project.

```
django-admin.py startproject playlist_connect_project
python manage.py startapp playlist_connect_api
```
To enable a newly created app, navigate to settings.py under the playlist_connect_project directory and:
    - add 'rest_framework' to INSTALLED_APPS
    - add 'rest_framework.authtoken' to INSTALLED_APPS
    - add {new_app_name} TO INSTALLED_APPS
    - add a trailing comma ',' at the end of each line

[playlistpair.com]: https://playlistpair.com
[vagrant]: https://www.vagrantup.com/downloads
[virtualbox]: https://www.virtualbox.org/wiki/Downloads
[git]: https://git-scm.com/downloads
[heroku playlistpair]: https://dashboard.heroku.com/apps/playlistpairapi
[heroku]: https://heroku.com/
[heroku cli]: https://devcenter.heroku.com/articles/heroku-cli
[Playlist Pair Frontend]: https://github.com/mcabrejos24/Playlist_Pair
