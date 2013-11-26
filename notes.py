from bottle import Bottle, route, run, template, request, static_file, error

import dbaccessor

DB = 'notes.db'

app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

@app.error(404)
def error404(error):
    return 'Nothing here, sorry'

@app.route('/')
def index():
    dba = dbaccessor.DbAccessor(DB)

    notes = dba.getAllNotes()

    return indexTemplate(notes, False)

@app.route('/new', method='GET')
def new():
    dba = dbaccessor.DbAccessor(DB)
    notes = dba.getAllNotes()

    return indexTemplate(notes, True)

@app.route('/new', method='POST')
def new():
    if request.POST.get('save','').strip():
        title = request.POST.get('title','').strip()
        content = request.POST.get('content','').strip()

        dba = dbaccessor.DbAccessor(DB)
        dba.addNote(title, content)

        notes = dba.getAllNotes()
        return indexTemplate(notes, False)

@app.route('/delete/:id', method='GET')
def delete_note(id):
    dba = dbaccessor.DbAccessor(DB)
    dba.deleteNote(id)
    notes = dba.getAllNotes()

    return indexTemplate(notes, False)

def indexTemplate(notes, isNew):
    output = template('index.tpl', rows=notes, new=isNew)
    return output

if __name__ == '__main__':
    app.run()
