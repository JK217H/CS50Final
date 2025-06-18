import sqlite3

# Connect to (or create) the database file
conn = sqlite3.connect('tasks.db')

# Create a cursor to run SQL commands
c = conn.cursor()

# Create a table for tasks
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT,
        tag TEXT,
        status TEXT NOT NULL
    )
''')
c.execute('''
            CREATE TABLE IF NOT EXISTS project_tags (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tag TEXT UNIQUE NOT NULL
    )       
''')
# Save changes and close the connection
conn.commit()
conn.close()
