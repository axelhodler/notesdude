from webtest import TestApp
import os
import re
import ConfigParser

import notes
import dbaccessor

import psycopg2

DB = 'test'
USER = 'xorrr'

CONFIG_FILE = 'user.cfg'

class TestWebserver():
    def login(self):
        config = ConfigParser.RawConfigParser()
        config.read(CONFIG_FILE)
        section = config.sections()[0]

        return self.bottle.post('/login', {'user': config.get(section, 'username'), 'password': config.get(section, 'password')})

    def check_if_logged_in(self, result):
        assert 'Logged in as: ' in result.body

    def check_index_route_after_login(self):
        result = self.login()
        result = self.bottle.get('/')

        # dont show the login part if you are already logged in
        # but show the button
        assert len(result.forms) == 4

        forms = result.forms
        assert forms[3].action == '/new'
        assert forms[3].method == 'POST'
        assert forms[3]['title'].value == ''
        assert forms[3]['content'].value == ''

    def setUp(self):
        self.bottle = TestApp(notes.SESSION)
        self.dba = dbaccessor.DbAccessor(DB, USER)

    def test_route_index(self):
        # after adding these two 4 forms will exist (two delete buttons, the
        # login and the add form
        self.dba.add_note('eins', 'lorem ipsum')
        self.dba.add_note('zwei', 'blabla')

        result = self.bottle.get('/')

        assert result.status == '200 OK'
        match = re.search(r'<td>blabla</td>\s*<td>', result.body)
        assert match

        assert 'href="static/css/bootstrap.min.css"' in result

        all_forms = result.forms
        assert len(all_forms) == 3

        login_form = all_forms[0]
        assert login_form.action == '/login'
        assert login_form.method == 'POST'
        assert login_form['user'].value == ''
        assert login_form['password'].value == ''

        self.check_index_route_after_login()

    def test_adding_new_note(self):
        self.login()
        result = self.bottle.get('/')
        new_note_form = result.forms[1]
        new_note_form['title'] = "testtitle"
        new_note_form['content'] = "testcontent"

        result = new_note_form.submit('save')
        assert result.status_int == 302

        notes = self.dba.get_all_notes()

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
        self.login()
        result = self.bottle.get('/')
        forms = result.forms
        assert forms[1].action == '/new'

        result = forms[1].submit()
        assert result.status == '200 OK'

    def test_deleting_note(self):
        self.dba.add_note('eins', 'lorem ipsum')

        result = self.bottle.get('/')
        assert 'value="Delete Note" disabled="disabled">' in result

        result = self.bottle.get('/delete/1', status=404)
        assert result.status_int == 404

        self.login()
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

        self.check_if_logged_in(result)

        result = self.bottle.get('/logout')
        assert result.status_int == 302

    def test_logout_button(self):
        result = self.login()
        result = self.bottle.get('/')

        forms = result.forms
        logout_form = forms[0]

        assert logout_form.action == '/logout'

        logout_form.submit()

        result = self.bottle.get('/')

        forms = result.forms

        login_form = forms[0]
        assert login_form.action == '/login'
        assert login_form.method == 'POST'

    def test_session(self):
        result = self.login()
        result = self.bottle.get('/login')

        self.check_if_logged_in(result)

        result = self.bottle.get('/login')

        self.check_if_logged_in(result)

    def tearDown(self):
        con = psycopg2.connect(database=DB, user=USER)
        cur = con.cursor()
        cur.execute("DROP TABLE IF EXISTS Notes")
        con.commit()
        con.close()
