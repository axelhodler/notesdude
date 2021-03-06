from webtest import TestApp

import psycopg2
import os
import urlparse

from notesdude.dbaccessor import DbAccessor

TABLE_NAME = "Notes"

class TestDbAccessor():
    def setUp(self):
        self.dba = DbAccessor()
        urlparse.uses_netloc.append("postgres")
        url = urlparse.urlparse(os.environ["DATABASE_URL"])

        self.con = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cur = self.con.cursor()

    def test_adding_note(self):
        self.dba.add_note('testtitle', 'testcontent')

        self.cur.execute('SELECT * FROM ' + TABLE_NAME)
        rows = self.cur.fetchone()

        assert rows[0] == 1
        assert rows[1] == 'testtitle'
        assert rows[2] == 'testcontent'

    def test_deleting_note(self):
        self.dba.add_note('testtitle', 'testcontent')

        self.dba.delete_note(1)

        self.cur.execute('SELECT * FROM ' + TABLE_NAME)
        rows = self.cur.fetchone()

        assert rows == None

    def test_getting_all_notes(self):
        self.dba.add_note('testtitle', 'testcontent')
        self.dba.add_note('testtitle2', 'testcontent2')

        notes = self.dba.get_all_notes()

        assert len(notes) == 2
        assert notes[0].get('id') == 1
        assert notes[0].get('title') == 'testtitle'
        assert notes[0].get('content') == 'testcontent'

        assert notes[1].get('id') == 2
        assert notes[1].get('title') == 'testtitle2'
        assert notes[1].get('content') == 'testcontent2'

    def test_getting_cursor(self):
        cursor = self.dba.get_cursor()
        assert isinstance(cursor, psycopg2._psycopg.cursor)

    def tearDown(self):
        self.cur.execute("DROP TABLE IF EXISTS " + TABLE_NAME)
        self.con.commit()
        self.con.close()
