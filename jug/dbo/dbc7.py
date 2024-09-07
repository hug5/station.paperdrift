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
        gLib.uwsgi_log("---disconnecting")

        if self.pool is not None:
            gLib.uwsgi_log("---disconnecting")
            self.pool.close()


        # When to close connection??



    def doQuery(self):

        # https://mariadb.com/docs/server/connect/programming-languages/python/example/
        gLib.uwsgi_log("---doQuery")
        # self.doConnect()
          # Create connection pool;


        # query = "SELECT * FROM ARTICLES $status_date ORDER BY DATETIME DESC LIMIT $start, $rows"
        # query = "SELECT * FROM ARTICLES LIMIT 1"
        # query = "SELECT * FROM ARTICLES"
        # query = "'SELECT first_name,last_name FROM employees WHERE first_name=?', (some_name,)"

        gLib.uwsgi_log("---get pool connection")

        self.doConnect()

        # if self.pool is None:
        #     gLib.uwsgi_log("---New Connect")
        #     self.doConnect()

        # else:
        #     # self.pool.connect()
        #     pool_connect = self.pool.get_connection()


        gLib.uwsgi_log("---here 1")
        try:
            # self.pool.connect()
            gLib.uwsgi_log("---here 2")

            pool_connect = self.pool.get_connection() ###

            gLib.uwsgi_log("---here 3")

        except mariadb.PoolError as e:
           gLib.uwsgi_log(f"---Error opening connection from pool: {e}")

        except Exception as e:
            gLib.uwsgi_log(f"---Error {e}")
            self.doConnect()
            pool_connect = self.pool.get_connection()



        gLib.uwsgi_log("---here 4")


        # try:
        #     # establish pool connection
        #     gLib.uwsgi_log("---try getting connection")
        #     pool_connect = self.pool.get_connection()
        # except:
        #     try:
        #         # self.doConnect()
        #         gLib.uwsgi_log("---trying pool.connect")
        #         self.pool.connect()
        #         pool_connect = self.pool.get_connection()


        #     except:
        #         # self.pool.add_connection()
        #         gLib.uwsgi_log("---trying new connect")
        #         self.doConnect()
        #         pool_connect = self.pool.get_connection()





        # instantiate the cursor
        # curs = self.db.cursor()
        curs = pool_connect.cursor()

        # https://mariadb-corporation.github.io/mariadb-connector-python/cursor.html
        curs.prepared = True
          # Not sure if you really need this?

        # result = curs.execute(query)
        # The result itself doesn't seem to be iterable; have to put into list??
        # I guess it doesn't really return anything??

        # Run the query;
        query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"

        gLib.uwsgi_log("---run query")

        curs.execute(query)


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


        # self.doDisconnect()
        pool_connect.close()
        return resultList



    #def static function doConnect($sphinx = false) {
    def doConnect(self):

        gLib.uwsgi_log("---Begin Connect")

        if self.pool:
            gLib.uwsgi_log("---already connected")
            return;


        gLib.uwsgi_log("---Connecting")
            
        un = "inkon"
        pw = "J##Dd*(r9TZYKh$%"
        host = "localhost"   # default
        port = 3306
        database = "inkonDb"
        autocommit = False
        
        pool_name = "pool_1"
        pool_size = 20
        pool_reset_connect = False
        pool_valid_int = 250
        
        try:
                
            self.pool = mariadb.ConnectionPool(
                user = un,
                password = pw,
                # host = host,
                port = port,
                database = database,
                # protocol = "SOCKET",
                autocommit = autocommit,

                pool_name=pool_name,
                pool_size=pool_size,
                pool_reset_connection = pool_reset_connect,
                pool_validation_interval = pool_valid_int

            )

        except mariadb.Error as e:
            # print(f"Error connecting to mariadb: {e}")
            return e

        finally:
            gLib.uwsgi_log("---Connected")




        # - - - - - - - - - - - - - -

            # if self.db:
            #     return;

            # $host     = F::json("config-admin", "host");
            # $database = F::json("config-admin", "database");
            # $un       = F::json("config-admin", "un");
            # $pw       = F::json("config-admin", "pw");
            # self::$Db = new \mysqli($host, $un, $pw, $database);
            # self::$Db->set_charset("utf8");

            # un = "inkon"
            # pw = "J##Dd*(r9TZYKh$%"
            # host = "localhost"   # default
            # port = 3306
            # database = "inkonDb"
            # autocommit = False

            # try:
            #     self.db = mariadb.connect(
            #         user = un,
            #         password = pw,
            #         # host = host,
            #         port = port,
            #         database = database,
            #         # protocol = "SOCKET",
            #         autocommit = autocommit
            #     )

            #     # return self.db

            # except mariadb.Error as e:
            #     # print(f"Error connecting to mariadb: {e}")
            #     return e