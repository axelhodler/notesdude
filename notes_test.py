from webtest import TestApp

import notes

def test_index():
    bottle = TestApp(notes.app)
    result = bottle.get('/')
    assert result.status == '200 OK'
    assert result.body == 'hello'
