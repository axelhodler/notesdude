from webtest import TestApp
import os
import re

import notes
import dbaccessor

DB = 'notes.db'

class TestWebserver():
    def test_index(self):
        dba = dbaccessor.DbAccessor(DB)
        dba.addNote('eins', 'lorem ipsum')
        dba.addNote('zwei', 'blabla')

        bottle = TestApp(notes.app)
        result = bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*</tr>', result.body)
        assert match

    def test_new(self):
        bottle = TestApp(notes.app)
        result = bottle.get('/new')
        assert result.status == '200 OK'
        form = result.form
        assert form.action == '/new'
        assert form.method == 'GET'
        assert form['title'].value == ''
        assert form['content'].value == ''

    def test_adding_new_note(self):
        bottle = TestApp(notes.app)
        result = bottle.get('/new')
        form = result.form
        form['title'] = "testtitle"
        form['content'] = "testcontent"

        result = form.submit('save')
        assert result.status == '200 OK'

    def tearDown(self):
        if os.path.isfile(DB):
            os.remove(DB)
