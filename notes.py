from bottle import Bottle, route, run, template, request, static_file, error, SimpleTemplate, response
from beaker.middleware import SessionMiddleware
import bottle
import dbaccessor

DB = 'notes.db'
USERNAME = 'xorrr'

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
    dba = dbaccessor.DbAccessor(DB)

    notes = dba.getAllNotes()

    return indexTemplate(notes, False, '')

@app.route('/new', method='GET')
def new():
    dba = dbaccessor.DbAccessor(DB)
    notes = dba.getAllNotes()

    return indexTemplate(notes, True, '../')

@app.route('/new', method='POST')
def new():
    if request.POST.get('save','').strip():
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()

        dba = dbaccessor.DbAccessor(DB)
        dba.addNote(title, content)

        notes = dba.getAllNotes()
        return indexTemplate(notes, False, '../')

@app.route('/delete/:id', method='GET')
def delete_note(id):
    dba = dbaccessor.DbAccessor(DB)
    dba.deleteNote(id)
    notes = dba.getAllNotes()

    return indexTemplate(notes, False, '../')

@app.route('/login', method='POST')
def login():
    if request.forms.get('user') == USERNAME:
        s = bottle.request.environ.get('beaker.session')
        s['user'] = request.forms.get('user')
        response.status = 200
    else:
        response.status = 404

@app.route('/login', method='GET')
def login():
    session = bottle.request.environ.get('beaker.session')
    logged_in = 'user' in session
    if logged_in:
        return 'Logged in as: %s' % session['user']
    else:
        return 'You are not logged in'

def indexTemplate(notes, isNew, toRoute):
    output = template('index.tpl', rows=notes, new=isNew, route=toRoute)
    return output

if __name__ == '__main__':
    bottle.run(app=session)
