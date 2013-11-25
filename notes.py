from bottle import Bottle, route, run

import dbaccessor

DB = 'notes.db'

app = Bottle()

@app.route('/')
def index():
    dba = dbaccessor.DbAccessor(DB)
    notes = dba.getAllNotes()

    return str(notes)

if __name__ == '__main__':
    app.run()
