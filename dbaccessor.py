import sqlite3
import os

class DbAccessor():
    def __init__(self, db_file_name):
        self.con = sqlite3.connect(db_file_name)
        self.cur = self.con.cursor()
        self.cur.execute('CREATE TABLE IF NOT EXISTS Notes(Id INTEGER PRIMARY KEY, Title TEXT, Content TEXT)')

    def get_all_notes(self):
        ''' returns a list with tuples '''
        self.cur.execute('SELECT * FROM Notes')
        rows = self.cur.fetchall()

        notes = []
        for row in rows:
            note = {}
            note['id'] = row[0]
            note['title'] = row[1]
            note['content'] = row[2]
            notes.append(note)

        return notes

    def add_note(self, title, content):
        note = (title, content)
        self.cur.execute('INSERT INTO Notes(Title, Content) VALUES(?,?)', note)

        self.con.commit()

    def delete_note(self, id):
        self.cur.execute('DELETE FROM Notes WHERE Id = ' + str(id))

        self.con.commit()

    def get_cursor(self):
        return self.cur
