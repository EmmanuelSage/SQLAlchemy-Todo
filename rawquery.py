import sqlite3

#connects it to the rawquery db and creates it if it does not exist
conn = sqlite3.connect('rawquery.db')

#creates the cursor
cur = conn.cursor()

#execute the query which creates the todo called test with id and name
#as the columns
cur.execute('''
    CREATE TABLE todo
    (id INTEGER PRIMARY KEY ASC,
     name varchar(250) NOT NULL)
''')

#executes the query which inserts values in the table
cur.execute("INSERT INTO test VALUES(1, 'The first todo is inputed into the database')")

#commits the executions
conn.commit()

#closes the connection
conn.close()