# https://dzone.com/articles/python-to-mariadb-connector
# https://mariadb.com/resources/blog/how-to-connect-python-programs-to-mariadb/
# https://mariadb.com/docs/server/connect/programming-languages/python/example/

# $ pip3 install mariadb

import mariadb

# Connect to Mariadb
try: 
    conn = mariadb.connect(
        user = "db_user",
        password = "db_user_passwd",
        host = "192.0.2.1",
        port = 3306,
        database = "employees",
        autocommit = False
    ) 
except mariadb.Error as e:
    print(f"Error connecting to mariadb: {e}")

# Disable Auto-Commit
# conn.autocommit = False

# get cursor
cur = conn.cursor()
# The cursor provides you with an interface for interacting with the Server, such as running SQL queries and managing transactions.

some_name = "Georgi"

cur.execute(
    "SELECT first_name,last_name FROM employees WHERE first_name=?", 
    (some_name,))

# Print Result-set
for (first_name, last_name) in cur: 
    print(f"First Name: {first_name}, Last Name: {last_name}")

# Put results into list:
contacts = []
# Prepare Contacts
for (first_name, last_name, email) in cur:
    contacts.append(f"{first_name} {last_name} <{email}>")

# List Contacts
print("\n".join(contacts))


# insert information
try:
    cursor.execute(
        "INSERT INTO employees (first_name,last_name) VALUES (?, ?)", 
        (first_name, last_name))
except mariadb.Error as e:
    print(f"Error: {e}")

conn.commit()

print(f"Last Inserted ID: {cur.lastrowid}") 


# commit()
# rollback()

# While inserting rows, you may want to find the Primary Key of the last inserted row when it is generated, as with auto-incremented values. You can retrieve this using the lastrowid() method on the cursor.

# Close Connection
conn.close()

