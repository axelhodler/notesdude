from webtest import TestApp
import os
import re

import notes
import dbaccessor

DB = 'notes.db'

class TestWebserver():
    def setUp(self):
        self.bottle = TestApp(notes.app)
        self.dba = dbaccessor.DbAccessor(DB)

    def test_route_index(self):
        self.dba.addNote('eins', 'lorem ipsum')
        self.dba.addNote('zwei', 'blabla')

        result = self.bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*<td>', result.body)
        assert match

    def test_route_new(self):
        result = self.bottle.get('/new')
        assert result.status == '200 OK'
        form = result.form
        assert form.action == '/new'
        assert form.method == 'POST'
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

        notes = self.dba.getAllNotes()

        assert len(notes) == 1
        assert notes[0].get('id') == 1
        assert notes[0].get('title') == 'testtitle'
        assert notes[0].get('content') == 'testcontent'

        assert '<p>Notes</p>' in result

    def test_accessing_static_file(self):
        result = self.bottle.get('/static/css/bootstrap.min.css')
        assert result.status == '200 OK'

    def test_nonexistent_route(self):
        # status=404 because i don't want the stacktrace and therefore
        # never get the result
        result = self.bottle.get('/foobar', status=404)
        assert result.status == '404 Not Found'
        assert result.body == 'Nothing here, sorry'

    def test_index_new_button(self):
        result = self.bottle.get('/new')
        form = result.form
        assert form.action == '/new'

        result = form.submit()
        assert result.status == '200 OK'

    def test_deleting_note(self):
        self.dba.addNote('eins', 'lorem ipsum')

        result = self.bottle.get('/delete/1')
        assert result.status == '200 OK'

    def tearDown(self):
        if os.path.isfile(DB):
            os.remove(DB)
