import sqlite3
import os

DB = 'test.db'

class TestSqlite():
    def setUp(self):
        ''' called before each test '''
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()
        self.cur.execute('DROP TABLE IF EXISTS Notes')
        self.cur.execute('CREATE TABLE Notes(Id INT, Title TEXT, Content TEXT)')

    def test_creating_DB(self):
        assert os.path.isfile(DB)

    def test_DB_version(self):
        self.cur.execute('SELECT SQLITE_VERSION()')
        version = self.cur.fetchone()
        assert str(version[0]) == '3.8.1'

    def test_deleting_note(self):
        self.cur.execute("INSERT INTO Notes VALUES(1, 'To Buy', 'Coffee')")
        self.cur.execute('SELECT * FROM Notes')

        rows = self.cur.fetchone()

        assert rows[0] == 1
        assert rows[1] == 'To Buy'
        assert rows[2] == 'Coffee'

        self.cur.execute("DELETE FROM Notes WHERE Id = 1")
        rows = self.cur.fetchone()
        assert rows == None

    def tearDown(self):
        ''' called after each test '''
        self.cur.execute('DROP TABLE IF EXISTS Notes')
        self.con.close()
        os.remove(DB)
