import sqlite3
import os

DB = 'test.db'

class DbAccessor():
    def __init__(self):
        self.con = sqlite3.connect(DB)
        self.cur = self.con.cursor()

    def getAllNotes(self):
        ''' returns a list with the notes as dictionaries '''
        notes = []

        self.cur.execute('SELECT * FROM Notes')
        rows = self.cur.fetchall()

        for row in rows:
            item = {}
            item['id'] = row[0]
            item['title'] = row[1]
            item['content'] = row[2]

            notes.append(item)

        return notes

    def addNote(self, title, content):
        note = (title, content)
        self.cur.execute('INSERT INTO Notes(Title, Content) VALUES(?,?)', note)

        self.con.commit()

    def deleteNote(self, id):
        self.cur.execute('DELETE FROM Notes WHERE Id = ' + str(id))

        self.con.commit()
