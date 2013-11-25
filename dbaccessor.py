import sqlite3
import os

class DbAccessor():
    def __init__(self, db_file_name):
        self.con = sqlite3.connect(db_file_name)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes(Id INTEGER PRIMARY KEY, Title TEXT, Content TEXT)')

    def getAllNotes(self):
        ''' returns a list with the notes as dictionaries '''
        notes = []

        self.cur.execute('SELECT * FROM Notes')
        rows = self.cur.fetchall()

        for row in rows:
            item = ()
            notes.append(row)

        return notes

    def addNote(self, title, content):
        note = (title, content)
        self.cur.execute('INSERT INTO Notes(Title, Content) VALUES(?,?)', note)

        self.con.commit()

    def deleteNote(self, id):
        self.cur.execute('DELETE FROM Notes WHERE Id = ' + str(id))

        self.con.commit()
