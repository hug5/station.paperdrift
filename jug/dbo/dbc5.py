# Module Import
import mariadb



# Create Connection Pool
def create_connection_pool():
    """Creates and returns a Connection Pool"""

    # Create Connection Pool
    pool = mariadb.ConnectionPool(
      host="192.0.2.1",
      port=3306,
      user="db_user",
      password="USER_PASSWORD",
      pool_name="web-app",
      pool_size=20,
      pool_reset_connection = False,
      pool_validation_interval=250   ##

    )

    # Return Connection Pool
    return pool

# Establish Pool Connection
try:
    pool = create_connection_pool()
    pconn = pool.get_connection()

    # Instantiate Cursor
    cur = pconn.cursor()

except mariadb.PoolError as e:
   # Report Error
   print(f"Error opening connection from pool: {e}")

   # Create New Connection as Alternate
   pconn = mariadb.connection(
      host="192.0.2.1",
      port=3306,
      user="db_user",
      password="db_user_password"
   )


  try:
      pool.add_connection(pconn)

  except mariadb.PoolError as e:

      # Report Error
      print(f"Error adding connection to pool: {e}")


pool.set_config(
    host="192.0.2.1",
    port=3306,
    user="db_user",
    password="USER_PASSWORD")

pool.add_connection()
pool.add_connection()
pool.add_connection()

conn = pool.get_connection()
