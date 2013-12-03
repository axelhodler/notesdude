from webtest import TestApp
import os
import re

import notes
import dbaccessor

DB = 'notes.db'

class TestWebserver():
    def setUp(self):
        self.bottle = TestApp(notes.session)
        self.dba = dbaccessor.DbAccessor(DB)

    def test_route_index(self):
        self.dba.addNote('eins', 'lorem ipsum')
        self.dba.addNote('zwei', 'blabla')

        result = self.bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*<td>', result.body)
        assert match

        assert 'href="static/css/bootstrap.min.css"' in result

    def test_route_new(self):
        result = self.bottle.get('/new')
        assert result.status == '200 OK'
        form = result.form
        assert form.action == '/new'
        assert form.method == 'POST'
        assert form['title'].value == ''
        assert form['content'].value == ''

        assert 'href="../static/css/bootstrap.min.css"' in result

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

        assert '<h1>Notes</h1>' in result
        assert 'href="../static/css/bootstrap.min.css"' in result

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
        forms = result.forms
        assert forms[0].action == '/new'

        result = forms[0].submit()
        assert result.status == '200 OK'

    def test_deleting_note(self):
        self.dba.addNote('eins', 'lorem ipsum')

        result = self.bottle.get('/delete/1')
        assert result.status == '200 OK'

        assert 'href="../static/css/bootstrap.min.css"' in result

    def test_login(self):
        result = self.bottle.post('/login', {'user': 'xorrr'})
        assert result.status_int == 200

        result = self.bottle.post('/login', {'user': 'xor'}, status=404)
        assert result.status_int == 404

    def test_logout(self):
        result = self.bottle.post('/login', {'user': 'xorrr'})
        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

        result = self.bottle.get('/logout')
        assert result.body == 'Successfully logged out'

        result = self.bottle.get('/logout')
        assert result.body == 'You are not logged in'

    def test_session(self):
        result = self.bottle.post('/login', {'user': 'xorrr'})
        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

    def tearDown(self):
        if os.path.isfile(DB):
            os.remove(DB)
