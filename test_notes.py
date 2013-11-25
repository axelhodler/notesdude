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
        assert result.body == "[(1, u'eins', u'lorem ipsum'), (2, u'zwei', u'blabla')]"

    def tearDown(self):
        os.remove(DB)
