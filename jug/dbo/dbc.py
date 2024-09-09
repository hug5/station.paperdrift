import mariadb
from jug.lib import gLib

class Dbc():

    def __init__(self):
        # self.db
        self.pool = None
        pass


    def commit_transaction(self):
        self.db.commit()


    def doDisconnect(self):

        # if self.db:
        #     self.db.close
            # self.db = False
        gLib.uwsgi_log("Disconnecting")

        if self.pool is not None:
            self.pool.close()
            self.pool = None
            gLib.uwsgi_log("Disconnected")
        # When to close connection??


    def doQuery(self, query):

        # https://mariadb.com/docs/server/connect/programming-languages/python/example/
        gLib.uwsgi_log("Begin Query")


        gLib.uwsgi_log("get pool connection")
        # Create connection pool;
        # self.doConnect()

        gLib.uwsgi_log("here 1")
        try:
            # self.pool.connect()
            gLib.uwsgi_log("here 2")

            # self.pool.add_connection()
            pool_connect = self.pool.get_connection() ###


        except mariadb.PoolError as e:
            gLib.uwsgi_log(f"Error opening connection from pool: {e}")
            self.pool.add_connection()
            pool_connect = self.pool.get_connection() ###

            # self.doDisconnect()
            # self.doConnect()
            # self.pool.add_connection()
            # pool_connect = self.pool.get_connection()

        except Exception as e:
            gLib.uwsgi_log(f"Error {e}")
            self.doDisconnect()
            self.doConnect()
            self.pool.add_connection()
            pool_connect = self.pool.get_connection()


        gLib.uwsgi_log("here 3")
        # instantiate the cursor
        # curs = self.db.cursor()
        curs = pool_connect.cursor()

        # pool_connect.begin()

        # https://mariadb-corporation.github.io/mariadb-connector-python/cursor.html
        # curs.prepared = True
          # Not sure if you really need this?

        # result = curs.execute(query)
        # The result itself doesn't seem to be iterable; have to put into list??
        # I guess it doesn't really return anything??

        gLib.uwsgi_log("run query")

        # Run the query;
        # query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"
        curs.execute(query)

        # pool_connect.commit()
        # pool_connect.rollback()


        resultList = []

        # Prepare result:

        # Method 1
        # for (ARTICLENO, HEADLINE, BLURB) in cur:
        #     resultList.append(f"{first_name} {last_name} <{email}>")

            # This should put everything in a list as a single string;
            # Could also use this method to create a dictionary; with the field name as the index;

        # Method 2
        for row in curs:
            # arr.append(f"{row}")  # This would probably be like above;
            resultList.append(row)
            # This should create multidimensional list;
            # Each field is a separate list item;



        cc = self.pool.connection_count
        ps = self.pool.pool_size
        gLib.uwsgi_log(f"connection count: {cc}")
        gLib.uwsgi_log(f"pool size: {ps}")

        pool_connect.close()

        # cc = self.pool.connection_count
        # ps = self.pool.pool_size
        # gLib.uwsgi_log(f"connection count2: {cc}")
        # gLib.uwsgi_log(f"pool size2: {ps}")

        # for x in range(10000000):
        #     y = "hello"

        # self.doDisconnect()
        return resultList


    def getConfig(self):

        return {
            "un" : "inkon",
            "pw" : "J##Dd*(r9TZYKh$%",
            "host" : "localhost",         # localhost is default
            "port" : 3306,
            "database" : "inkonDb",
            "autocommit" : True,
            "pool_name" : "pool_1",
            "pool_size" : 64,             # The max should be 64
            "pool_reset_connect" : False,
            "pool_valid_int" : 500,       # 500 is default
        }

        # return config_dict

    def doConnect(self):

        gLib.uwsgi_log("Begin Connect")

        # if self.pool is not None:
        #     gLib.uwsgi_log("Already Connected")
        #     return;

        pool_conf = self.getConfig()

        gLib.uwsgi_log("Connecting")
        
        try:
            gLib.uwsgi_log("begin try connect")
                
            self.pool = mariadb.ConnectionPool(
                pool_name = pool_conf["pool_name"],
                pool_size = pool_conf["pool_size"],
                pool_reset_connection = pool_conf["pool_reset_connect"],
                pool_validation_interval = pool_conf["pool_valid_int"]
            )
            self.pool.set_config(
                user = pool_conf["un"],
                password = pool_conf["pw"],
                # host = host,
                port = pool_conf["port"],
                database = pool_conf["database"],
                # protocol = "SOCKET",
                autocommit = pool_conf["autocommit"],
            )

            # Create an initial connection pool slot
            # If we free up after every query, should be able to reuset his repeatedly and never exceed connection_count=1
            # Might need more if there are simultaneous connections?
            self.pool.add_connection()

            gLib.uwsgi_log("end try connect")

        except mariadb.Error as e:
            # print(f"Error connecting to mariadb: {e}")
            return e

        finally:
            gLib.uwsgi_log("Connected")

