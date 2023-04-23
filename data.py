import sqlite3
import sys

class Database:

    conn = None

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            if self.conn == None:
                raise ConnectionError("Error connecting to database")
            self.create_transactions_table()
        except (sqlite3.Error,ConnectionError) as e:
            print(e, file=sys.stderr)

    def create_transactions_table(self):
        """Create a table from the create_table_sql statement.
        """
        sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS transactions (
                                        id integer PRIMARY KEY,
                                        date text,
                                        value float,
                                        currency text,
                                        desc text,
                                        categ text
                                    ); """
        c = self.conn.cursor()
        c.execute(sql_create_transactions_table)

        