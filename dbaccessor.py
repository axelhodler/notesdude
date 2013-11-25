import sqlite3
import os

DB = 'test.db'

class DbAccessor():
    def addNote(self, title, content):
        con = sqlite3.connect(DB)
        cur = con.cursor()

        note = (title, content)
        cur.execute('INSERT INTO Notes(Title, Content) VALUES(?,?)', note)

        con.commit()
        cur.close()
