from bottle import Bottle, route, run, template

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
    return 'hello'

if __name__ == '__main__':
    app.run()
