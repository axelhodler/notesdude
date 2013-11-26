from webtest import TestApp
import os
import re

import notes
import dbaccessor

DB = 'notes.db'

class TestWebserver():
    def setUp(self):
        self.bottle = TestApp(notes.app)

    def test_route_index(self):
        dba = dbaccessor.DbAccessor(DB)
        dba.addNote('eins', 'lorem ipsum')
        dba.addNote('zwei', 'blabla')

        result = self.bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*</tr>', result.body)
        assert match

    def test_route_new(self):
        result = self.bottle.get('/new')
        assert result.status == '200 OK'
        form = result.form
        assert form.action == '/new'
        assert form.method == 'GET'
        assert form['title'].value == ''
        assert form['content'].value == ''

    def test_adding_new_note(self):
        result = self.bottle.get('/new')
        form = result.form
        form['title'] = "testtitle"
        form['content'] = "testcontent"

        result = form.submit('save')
        assert result.status == '200 OK'

        # check if has been added to the DB
        dba = dbaccessor.DbAccessor(DB)
        notes = dba.getAllNotes()

        assert len(notes) == 1
        assert notes[0][0] == 1
        assert notes[0][1] == 'testtitle'
        assert notes[0][2] == 'testcontent'

        assert result.body == "Note with id: 1 was added"

    def test_accessing_static_file(self):
        result = self.bottle.get('/static/css/bootstrap.min.css')
        assert result.status == '200 OK'

    def test_nonexistent_route(self):
        # status=404 because i don't want the stacktrace and therefore
        # never get the result
        result = self.bottle.get('/foobar', status=404)
        assert result.status == '404 Not Found'
        assert result.body == 'Nothing here, sorry'

    def tearDown(self):
        if os.path.isfile(DB):
            os.remove(DB)
