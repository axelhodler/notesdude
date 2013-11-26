from bottle import Bottle, route, run, template, request, static_file

import dbaccessor

DB = 'notes.db'

app = Bottle()

@app.route('/static/<filepath:path>')
def server_static(filepath):
    return static_file(filepath, root='./static')

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
        noteid = dba.getCursor().lastrowid

        return "Note with id: " + str(noteid) + " was added"
    else:
        output = template('new_note.tpl')
        return output

if __name__ == '__main__':
    app.run()
