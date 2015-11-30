#!/usr/bin/env python2.7
# encoding: utf-8
import sys
import os
import bottle
import simplejson
from bottle import request
from beaker.middleware import SessionMiddleware

# local
import template
from read_config import read_server_config
import repository
import webserver_session

# Location of all configuration files to use.
# Overwrite using additional command line arguments.
package_directory = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILES = [os.path.join(package_directory, './webserver.cfg')]

# Read the configuration
config_files = CONFIG_FILES
if __name__ == '__main__':
    if len(sys.argv) > 1:
        config_files = sys.argv[1:]
    print 'Reading from config files:', config_files
config = read_server_config(config_files)

bottle.BaseRequest.MEMFILE_MAX = 1024 * 1024

app = bottle.Bottle(autojson=True)
cache = [None]  # must be a list because of python 2.7

Repository = repository.Repository(config['db']['host'], config['db']['user'], config['db']['password'],
                                   config['db']['default_db'],
                                   port=config['db']['port'])


def get_session():
    s = bottle.request.environ.get('beaker.session')
    return webserver_session.Session(s)


def augment(f):
    '''Decorator to always pass certain variables to a dict result.

    Useful for adding information to templates, such as if the user is logged in.

    Read the code to see how to extend the navbar
    '''

    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        s = get_session()
        if s.page_message is not None and get_session().page_message is not '':
            result['message'] = s.page_message
            s.set_page_message('')

        if s.is_logged_in():
            result['username'] = s.username

        # if 'hide_sidebar' not in result:
            # result['leaderboard'] = 'something'
            # result['leaderboard'] = Repository.fetch_leaderboard()


            #fetch leaderboard
            #result['leaderboard'] = Repository.

        # if isinstance(result, dict):
        # Put here some last minute info, that you always need. E.g. if the user is logged in...

        return result

    return wrapper


def view(*args, **kwargs):
    '''Returns a decorator that takes a template name'''

    def wrapper(f):
        return template.view(*args, **kwargs)(augment(f))

    return wrapper


@app.error(500)
@view("500")
def custom500(error):
    url = bottle.request.url
    user_agent = bottle.request.environ['HTTP_USER_AGENT']
    post_data = request.POST.dict
    return dict(
        traceback=error.traceback
    )


@app.route('/generateerror')
def generate_error():
    return 1 / 0  # this will throw an error


@app.error(404)
@view("404")
def custom404(error):
    return dict(
    )


@app.error(403)
@view("403")
def custom403(event):
    return dict()


@app.route('/')
@view('home')
def home():
    if get_session().is_logged_in():
        bottle.redirect('/prediction')
        return dict()
    return dict()


@app.post('/')
@view('home')
def login():
    username = request.forms.get('login-username')
    password = request.forms.get('login-password')
    success, user_id = Repository.check_login(username, password)
    if not success:
        get_session().set_page_message('Invalid credentials')
        return dict()

    get_session().login(user_id, username)
    bottle.redirect('/prediction')
    return dict()


@app.get('/logout')
@view('home')
def logout():
    get_session().logout()
    get_session().set_page_message('You have been successfully logged out')
    bottle.redirect('/')
    return dict()

@app.route('/register')
@view('register')
def register():
    return dict(
        username=''
    )


@app.post('/register')
@view('register')
def save_user():
    username = request.forms.get('register-username')
    result = dict(
        username=username,
    )

    if username.strip() == '':
        get_session().set_page_message('A user with this login name already exists')
        return result

    if Repository.get_user(username) is not None:
        get_session().set_page_message('A user with this login name already exists')
        return result

    password = request.forms.get('register-password')
    password_confirmation = request.forms.get('register-password_confirmation')

    if password != password_confirmation:
        get_session().set_page_message('Passwords do not match')
        return result

    is_registered, user_id = Repository.register(username, password)
    if is_registered is True:
        get_session().login(user_id, username)
        bottle.redirect('/prediction')
        return result

    return result


@app.route('/prediction')
@view('prediction')
def prediction():
    if not get_session().is_logged_in():
        bottle.redirect('/')
        return dict()
    return dict()


@app.route('/twitter/user/<id:int>')
@view('twitter_user')
def load_twitter_user(id):
    twitter_user = Repository.fetch_twitter_user(id)

    return dict(
        id= id,
        user= twitter_user,
        hide_sidebar=True
    )


@app.route('/loading')
@view('loading')
def loading():
    return dict()

@app.route('/static/<filepath:path>')  # this can be removed
def serve_static(filepath):
    return bottle.static_file(filepath, root='./static/')


# =========================API===========================
def json_response(func):
    '''Use this decorator to create a json response for lists.
    Dictionaries are supported by default.
    '''

    def wrap(*args, **kwargs):
        bottle.response.content_type = 'application/json'
        result = func(*args, **kwargs)
        return simplejson.dumps(result, ensure_ascii=False)

    return wrap


@app.post('/api/gender/save')
@json_response
def save_gender():
    json = request.json
    gender = json['gender']
    twitter_id = json['id']
    result = {'message': 'ok'}

    if gender.strip() == '':
        result['message'] = 'data missing'

    if not get_session().is_logged_in():
        result['message'] = 'user is not logged in'
        return result

    Repository.save_user_prediction(get_session().user_id, twitter_id, gender)

    twitter_user = Repository.fetch_next_twitter_user(get_session().user_id)
    if twitter_user is None:
        result['message'] = 'last one'
        return result
    result['id'] = twitter_user['tus_id']
    result['twitter_screenname'] = twitter_user['tus_screenname']
    result['progress'] = Repository.fetch_progress()
    return result


@app.get('/api/twitter_user/get')
@json_response
def get_next_twitter_user():
    result = {'message': 'ok'}
    if not get_session().is_logged_in():
        result['message'] = 'user is not logged in'
        return result
    twitter_user = Repository.fetch_next_twitter_user(get_session().user_id)
    if twitter_user is None:
        result['message'] = 'last one'
        return result
    progress = Repository.fetch_progress()
    result['id'] = twitter_user['tus_id']
    result['twitter_screenname'] = twitter_user['tus_screenname']
    result['progress'] = progress
    return result

@app.get('/api/leaderboard/get')
@json_response
def get_leaderboard():
    result = None
    if not get_session().is_logged_in():
        result =  {'message' : 'user is not logged in'}
        return result
    else :
        result = {'message' : 'OK'}

    leaderboard = Repository.fetch_leaderboard()
    result['leaderboard'] = leaderboard 
    return result


# Add sessions using beaker middleware
# Keep here: app should not be overwritten initially
# http://beaker.readthedocs.org/en/latest/configuration.html
session_opts = {
    # Defaults to never expiring.
    # 'session.cookie_expires': 300,
    'session.auto': True
}
app = SessionMiddleware(app, session_opts)

if __name__ == '__main__':
    print 'Running with the following configuration:'
    print simplejson.dumps(config, indent=4)
    bottle.run(app, **config['server'])




