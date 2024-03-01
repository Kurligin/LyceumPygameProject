import sqlite3 as lite


class DatabaseManager(object):
    def __init__(self, path):
        self.conn = lite.connect(path)
        self.conn.execute('pragma foreign_keys = on')
        self.conn.commit()
        self.cur = self.conn.cursor()

        self.create_tables()

    def create_tables(self):
        self.query('CREATE TABLE IF NOT EXISTS config (record int)')

    def query(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        self.conn.commit()

    def fetchone(self, arg, values=None):
        if values is None:
            self.cur.execute(arg)
        else:
            self.cur.execute(arg, values)
        return self.cur.fetchone()

    def check_record(self, count):
        prev_record = self.fetchone('SELECT * FROM config')

        if prev_record:
            prev_record = int(prev_record[0])

            if prev_record < count:
                self.query('UPDATE config SET record = ?', (count,))
        else:
            self.query('INSERT INTO config VALUES (?)', (0,))

    def __del__(self):
        self.conn.close()
