import sqlite3
import mysql.connector

# SQLite connection
sqlite_conn = sqlite3.connect('instance/database.db')
sqlite_cursor = sqlite_conn.cursor()

# MySQL connection
mysql_conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='Radhekrishn..',
    database='recipe'
)
mysql_cursor = mysql_conn.cursor()

# Function to migrate data
def migrate_data():
    # Example: Migrate users table
    sqlite_cursor.execute("SELECT * FROM users")
    users = sqlite_cursor.fetchall()

    for user in users:
        mysql_cursor.execute("INSERT INTO users (id, name, email) VALUES (%s, %s, %s)", user)

    mysql_conn.commit()

# Run migration
migrate_data()

# Close connections
sqlite_conn.close()
mysql_conn.close()
print("Data migration completed successfully!")
