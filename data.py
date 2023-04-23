import sqlite3
import sys

class Database:

    conn = None
    transactions = []

    def __init__(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            if self.conn == None:
                raise ConnectionError("Error connecting to database")
            self.create_transactions_table()
            self.fetch_transactions()
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
    
    def fetch_transactions(self):
        with self.conn as c:
            cur = c.cursor()
            cur.execute('''SELECT * FROM transactions''')
            for tr in cur.fetchall():
                self.transactions.append(Transaction(tr))
    
    def dump_transactions(self):
        for tr in self.transactions:
            print(tr.__dict__)

class Transaction:
    id: int
    date: str
    value: float
    currency: str
    description: str
    category: str

    def __init__(self,raw_transaction):
        self.id = int(raw_transaction[0])
        self.date = raw_transaction[1]
        self.value = float(raw_transaction[2])
        self.currency = raw_transaction[3]
        self.desc = raw_transaction[4]
        self.categ = raw_transaction[5]
