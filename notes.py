from bottle import Bottle, route, run, template, request, static_file, error, SimpleTemplate, response, redirect
from beaker.middleware import SessionMiddleware
import bottle
import dbaccessor

DB = 'notes.db'
USERNAME = 'xorrr'
PASSWORD = 'test'

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}

app = Bottle()
session = SessionMiddleware(app, session_opts)

SimpleTemplate.defaults["get_url"] = app.get_url

@app.route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='static')

@app.error(404)
def error404(error):
    return 'Nothing here, sorry'

@app.route('/')
def index():
    session = get_session()
    logged_in = 'user' in session

    dba = dbaccessor.DbAccessor(DB)
    notes = dba.get_all_notes()

    if logged_in:
        return index_template(notes, session['user'], '')
    else:
        return index_template(notes, None, '')

@app.route('/new', method='POST')
def new():
    if request.POST.get('save','').strip():
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()

        dba = dbaccessor.DbAccessor(DB)
        dba.add_note(title, content)

        redirect("/")

@app.route('/delete/:id', method='GET')
def delete_note(id):
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        dba = dbaccessor.DbAccessor(DB)
        dba.delete_note(id)
        redirect("/")
    else:
        response.status = 404

@app.route('/login', method='POST')
def login():
    if request.forms.get('user') == USERNAME and request.forms.get('password') == PASSWORD:
        s = get_session()
        s['user'] = request.forms.get('user')
        redirect("/")
    else:
        response.status = 404

@app.route('/login', method='GET')
def login():
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        return 'Logged in as: %s' % session['user']
    else:
        return 'You are not logged in'

@app.route('/logout', method='GET')
def logout():
    session = get_session()
    logged_in = 'user' in session
    if logged_in:
        session.delete()
        redirect('/')

def index_template(notes, user, toRoute):
    output = template('index.tpl', rows=notes, user=user, route=toRoute)
    return output

def get_session():
    return bottle.request.environ.get('beaker.session')

if __name__ == '__main__':
    bottle.run(app=session)
