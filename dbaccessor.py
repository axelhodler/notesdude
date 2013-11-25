import sqlite3
import os

DB = 'test.db'

class DbAccessor():
    def __init__(self):
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()

    def addNote(self, title, content):
        note = (title, content)
        self.cur.execute('INSERT INTO Notes(Title, Content) VALUES(?,?)', note)

        self.con.commit()

    def deleteNote(self, id):
        self.cur.execute('DELETE FROM Notes WHERE Id = ' + str(id))

        self.con.commit()
