from bottle import Bottle, route, run, template, request, static_file, error, SimpleTemplate, response, redirect
from beaker.middleware import SessionMiddleware
import os
import bottle
import dbaccessor
import ConfigParser

CONFIG_FILE = 'user.cfg'

SESSION_OPTS = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

APP = Bottle()
SESSION = SessionMiddleware(APP, SESSION_OPTS)

@APP.route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='static')

@APP.error(404)
def error404(error):
    return 'Nothing here, sorry'

@APP.route('/')
def index():
    return build_index_template();

@APP.route('/new', method='POST')
def new():
    if request.POST.get('save','').strip():
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()

        dba = dbaccessor.DbAccessor()
        dba.add_note(title, content)

        redirect("/")

@APP.route('/delete/:note_id', method='GET')
def delete_note(note_id):
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        dba = dbaccessor.DbAccessor()
        dba.delete_note(note_id)
        redirect("/")
    else:
        response.status = 404

@APP.route('/login', method='POST')
def login():
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_FILE)
    config_section = config.sections()[0]
    session = get_session()
    if request.forms.get('user') == config.get(config_section, 'username') and request.forms.get('password') == config.get(config_section, 'password'):
        session['user'] = request.forms.get('user')
    else:
        session['fail'] = 'failed'
    redirect("/")

@APP.route('/login', method='GET')
def login():
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        return 'Logged in as: %s' % session['user']
    else:
        return 'You are not logged in'

@APP.route('/logout', method='GET')
def logout():
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        session.delete()
        redirect('/')

def build_index_template():
    session = get_session()
    logged_in = 'user' in session
    login_failed = 'fail' in session

    dba = dbaccessor.DbAccessor()
    notes = dba.get_all_notes()

    output = template('index.tpl', rows=notes, is_logged_in=logged_in, has_failed=login_failed)
    return output

def get_session():
    return bottle.request.environ.get('beaker.session')

if __name__ == '__main__':
    bottle.run(app=SESSION, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
