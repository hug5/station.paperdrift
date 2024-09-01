# https://mariadb.com/docs/server/connect/programming-languages/python/connect/

# Module Import
import mariadb
import sys

# Instantiate Connection
try:
   conn = mariadb.connect(
      host="192.0.2.1,192.0.2.0,198.51.100.0",
      port=3306,
      user="db_user",
      password="USER_PASSWORD")
   conn.auto_reconnect = True
except mariadb.Error as e:
   print(f"Error connecting to the database: {e}")
   sys.exit(1)

# Use Connection
# ...

# Close Connection
conn.close()



# Connection Failover
# Starting with MariaDB Connector/Python 1.1, when MariaDB Connector/Python is built with MariaDB Connector/C 3.3, the connector supports connection failover when auto_reconnect is enabled and the connection string contains a comma-separated list of multiple server addresses.
# To enable connection failover:
    # Call the mariadb.connect function with the host argument specified as a comma-separated list containing multiple server addresses. The connector attempts to connect to the addresses in the order specified in the list.
    # Set auto_reconnect to True. If the connection fails, the connector will attempt to reconnect to the addresses in the order specified in the list.

#-------------------

# Function / Description

# Connection
  # Represents a connection to a MariaDB database product.
# connect()
  # Establishes a connection to a database server and returns a connection object.
# cursor()
  # Returns a new cursor object for the current connection.
# change_user()
  # Changes the user and default database of the current connection.
# reconnect()
  # Tries to make a connection object active again by reconnecting to the server using the same credentials which were specified in connect() method.
# close()
  # Closes the connection.