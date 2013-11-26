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

    output = template('index.tpl', rows=notes)
    return output

@app.route('/new')
def new():
    if request.GET.get('save','').strip():
        title = request.GET.get('title','').strip()
        content = request.GET.get('content','').strip()

        dba = dbaccessor.DbAccessor(DB)
        dba.addNote(title, content)

        notes = dba.getAllNotes()
        output = template('index.tpl', rows=notes)
        return output
    else:
        output = template('new_note.tpl')
        return output

@app.route('/delete/:id', method='GET')
def delete_note(id):
    dba = dbaccessor.DbAccessor(DB)
    dba.deleteNote(id)
    notes = dba.getAllNotes()

    output = template('index.tpl', rows=notes)
    return output

if __name__ == '__main__':
    app.run()
