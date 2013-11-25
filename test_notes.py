from webtest import TestApp
import os

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
        assert result.body == "[{'content': u'lorem ipsum', 'id': 1, 'title': u'eins'}, {'content': u'blabla', 'id': 2, 'title': u'zwei'}]"

    def tearDown(self):
        os.remove(DB)
