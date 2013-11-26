from bottle import Bottle, route, run, template, request

import dbaccessor

DB = 'notes.db'

app = Bottle()

@app.route('/')
def index():
    dba = dbaccessor.DbAccessor(DB)

    notes = dba.getAllNotes()

    output = template('templates/index.tpl', rows=notes)
    return output

@app.route('/new')
def new():
    if request.GET.get('save','').strip():
        return "saved"
    else:
        output = template('templates/new_note.tpl')
        return output

if __name__ == '__main__':
    app.run()
