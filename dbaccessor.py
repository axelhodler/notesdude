import sqlite3
import os

DB = 'test.db'

class DbAccessor():
    def addNote(self, id, title, content):
        con = sqlite3.connect(DB)
        cur = con.cursor()

        note = (id, title, content)
        cur.execute('INSERT INTO Notes VALUES(?,?,?)', note)

        con.commit()
        cur.close()
