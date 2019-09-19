import sqlite3



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return None

def select_all_transactions(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM transactions")

    rows = cur.fetchall()
    for row in rows:
        print(row)


def select_transactions(conn, date_from, date_to, *args):
    """
    """
    cur = conn.cursor()
    if len(args) == 0:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}'
                        AND '{date_to}' ORDER BY date  ''')
    if len(args) == 1:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}' AND '{date_to}'
                        AND (type = '{args[0]}' OR '{args[0]}' = 'All')
                        ORDER BY date  ''')
    if len(args) == 3:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}' AND '{date_to}'
                        AND value BETWEEN '{args[0]}' AND '{args[1]}'
                        AND (type = '{args[2]}' OR '{args[2]}' = 'All')
                        ORDER BY date  ''')

    return cur.fetchall()



def get_balance(conn, date_from, date_to, *args):
    """
    """
    cur = conn.cursor()
    if len(args) == 0:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}'
                        AND '{date_to}' ORDER BY date  ''')
    if len(args) == 1:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}' AND '{date_to}'
                        AND (type = '{args[0]}' OR '{args[0]}' = 'All')
                        ORDER BY date  ''')
    if len(args) == 3:
        cur.execute(f'''SELECT * FROM transactions 
                        WHERE date BETWEEN '{date_from}' AND '{date_to}'
                        AND value BETWEEN '{args[0]}' AND '{args[1]}'
                        AND (type = '{args[2]}' OR '{args[2]}' = 'All')
                        ORDER BY date  ''')

    rows = cur.fetchall()
    total = 0
    expenses = 0
    income = 0
    multiplier = 1
    for row in rows:
        if row[3] == "£":
            multiplier = 1
        elif row[3] == "€":
            multiplier = 0.9
        elif row[3] == "$":
            multiplier = 0.8
        total += float(row[2])*multiplier
        if float(row[2]) > 0:
            income += row[2]*multiplier
        else:
            expenses += row[2]*multiplier

    return f"Spent: {expenses:.2f}£\nReceived: {income:.2f}£\nTotal balance: {total:.2f}£"



def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)
def create_transaction(conn, transaction):
    """
    Create a new project into the projects table
    :param conn:
    :param transaction:
    :return: project id
    """
    sql = ''' INSERT INTO transactions(date,value,currency,desc,type)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, transaction)

def main():
    database = "mydatabase.db"
    sql_create_transactions_table = """ CREATE TABLE IF NOT EXISTS transactions (
                                        id integer PRIMARY KEY,
                                        date text,
                                        value float,
                                        currency text,
                                        desc text,
                                        type text
                                    ); """

    # create a database connection
    conn = create_connection(database)

    if conn is not None:
        # create transactions table
        create_table(conn, sql_create_transactions_table)

    else:
        print("Error! cannot create the database connection.")
    with conn:

        select_all_transactions(conn)

if __name__ == '__main__':
    main()
