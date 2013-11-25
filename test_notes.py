from webtest import TestApp

import notes

class TestWebserver():
    def test_index(self):
        bottle = TestApp(notes.app)
        result = bottle.get('/')
        assert result.status == '200 OK'
        assert result.body == 'hello'
