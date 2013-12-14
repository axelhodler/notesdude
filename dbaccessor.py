import psycopg2
import os
import urlparse

class DbAccessor():
    def __init__(self):
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
        self.cur.execute("CREATE TABLE IF NOT EXISTS Notes(Id SERIAL PRIMARY KEY, Title TEXT, Content TEXT)")
        self.con.commit()

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

        # always commit open SELECTs or issues will arise
        self.con.commit()

        return notes

    def add_note(self, title, content):
        note = (title, content)
        query = "INSERT INTO Notes(Title, Content) VALUES(%s, %s)"
        self.cur.execute(query, note)
        self.con.commit()

    def delete_note(self, id):
        self.cur.execute('DELETE FROM Notes WHERE Id = ' + str(id))
        self.con.commit()

    def get_cursor(self):
        return self.cur
