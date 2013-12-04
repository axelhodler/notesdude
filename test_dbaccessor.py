from webtest import TestApp

import sqlite3
import os

import dbaccessor

DB = 'test.db'

class TestDbAccessor():
    def setUp(self):
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS Notes')
        self.cur.execute('CREATE TABLE Notes(Id INTEGER PRIMARY KEY, Title TEXT, Content TEXT)')

        self.dba = dbaccessor.DbAccessor(DB)

    def test_adding_note(self):
        self.dba.add_note('testtitle', 'testcontent')

        self.cur.execute('SELECT * FROM Notes')
        rows = self.cur.fetchone()

        assert rows[0] == 1
        assert rows[1] == 'testtitle'
        assert rows[2] == 'testcontent'

    def test_deleting_note(self):
        self.dba.add_note('testtitle', 'testcontent')

        self.dba.delete_note(1)

        self.cur.execute('SELECT * FROM Notes')
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
        assert isinstance(cursor, sqlite3.Cursor)

    def tearDown(self):
        self.cur.execute('DROP TABLE IF EXISTS Notes')
        self.con.close()
        os.remove(DB)
