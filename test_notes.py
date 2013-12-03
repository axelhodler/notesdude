from webtest import TestApp
import os
import re

import notes
import dbaccessor

DB = 'notes.db'

class TestWebserver():
    def login(self):
        return self.bottle.post('/login', {'user': 'xorrr', 'password': 'test'})

    def setUp(self):
        self.bottle = TestApp(notes.session)
        self.dba = dbaccessor.DbAccessor(DB)

    def test_route_index(self):
        # after adding these two 4 forms will exist (two delete buttons, the
        # login and the add form
        self.dba.addNote('eins', 'lorem ipsum')
        self.dba.addNote('zwei', 'blabla')

        result = self.bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*<td>', result.body)
        assert match

        assert 'href="static/css/bootstrap.min.css"' in result

        form = result.forms

        assert form[3].action == '/new'
        assert form[3].method == 'POST'
        assert form[3]['title'].value == ''
        assert form[3]['content'].value == ''

        login_form = form[0]
        assert login_form.action == '/login'
        assert login_form.method == 'POST'
        assert login_form['user'].value == ''
        assert login_form['password'].value == ''

        result = self.login()
        result = self.bottle.get('/')

        # dont show the login part if you are already logged in
        # but show the button
        assert len(result.forms) == 4

    def test_adding_new_note(self):
        result = self.bottle.get('/')
        new_note_form = result.forms[1]
        new_note_form['title'] = "testtitle"
        new_note_form['content'] = "testcontent"

        result = new_note_form.submit('save')
        assert result.status_int == 302

        notes = self.dba.getAllNotes()

        assert len(notes) == 1
        assert notes[0].get('id') == 1
        assert notes[0].get('title') == 'testtitle'
        assert notes[0].get('content') == 'testcontent'

        result = self.bottle.get('/')

        assert '<h1>Notes</h1>' in result
        assert 'href="static/css/bootstrap.min.css"' in result

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
        result = self.bottle.get('/')
        forms = result.forms
        assert forms[1].action == '/new'

        result = forms[1].submit()
        assert result.status == '200 OK'

    def test_deleting_note(self):
        self.dba.addNote('eins', 'lorem ipsum')

        result = self.bottle.get('/delete/1')
        assert result.status_int == 302

    def test_login(self):
        result = self.login()
        assert result.status_int == 302

        result = self.bottle.post('/login', {'user': 'xor'}, status=404)
        assert result.status_int == 404

        result = self.bottle.post('/login', {'user': 'xorrr', 'password': 'wrong'}, status=404)
        assert result.status_int == 404

    def test_logout(self):
        result = self.login()
        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

        result = self.bottle.get('/logout')
        assert result.body == 'Successfully logged out'

        result = self.bottle.get('/logout')
        assert result.body == 'You are not logged in'

    def test_logout_button(self):
        result = self.login()
        result = self.bottle.get('/')

        forms = result.forms
        logout_form = forms[0]

        assert logout_form.action == '/logout'

    def test_session(self):
        result = self.login()
        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

        result = self.bottle.get('/login')

        assert result.body == 'Logged in as: xorrr'

    def tearDown(self):
        if os.path.isfile(DB):
            os.remove(DB)
