from jug.lib.logger import logger

import mariadb
# from jug.lib import gLib

class Dbc():

    def __init__(self):
        # self.db
        self.pool = None
        pass


    def commit_transaction(self):
        # self.db.commit()
        pass


    def doDisconnect(self):

        # if self.db:
        #     self.db.close
            # self.db = False
        # gLib.uwsgi_log("Disconnecting")
        logger.info('Disconnecting')

        if self.pool is not None:
            self.pool.close()
            self.pool = None
            # gLib.uwsgi_log("Disconnected")
            # logger.info('Disconnected')
        # When to close connection??


    def doQuery(self, query):

        # https://mariadb.com/docs/server/connect/programming-languages/python/example/
        # gLib.uwsgi_log("Begin Query")
        logger.info('Begin Query + get pool connection')


        # gLib.uwsgi_log("get pool connection")
        logger.info('get pool connection')
        # Create connection pool;
        # self.doConnect()

        # logger.info("here 1")
        try:
            # self.pool.connect()
            # logger.info("here 2")

            # self.pool.add_connection()
            pool_connect = self.pool.get_connection() ###


        except mariadb.PoolError as e:
            logger.info(f"Error opening connection from pool: {e}")
            self.pool.add_connection()
            pool_connect = self.pool.get_connection() ###

            # self.doDisconnect()
            # self.doConnect()
            # self.pool.add_connection()
            # pool_connect = self.pool.get_connection()

        except Exception as e:
            logger.error(f"Error {e}")

            self.doDisconnect()
            self.doConnect()
            self.pool.add_connection()
            pool_connect = self.pool.get_connection()


        # logger.info("here 3")
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

        logger.info("run query")

        # Run the query;
        # query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"
        curs.execute(query)

        # pool_connect.commit()
        # pool_connect.rollback()

        ##########
                # resultList = []

                # # Prepare result:

                # # Method 1
                # # for (ARTICLENO, HEADLINE, BLURB) in cur:
                # #     resultList.append(f"{first_name} {last_name} <{email}>")

                #     # This should put everything in a list as a single string;
                #     # Could also use this method to create a dictionary; with the field name as the index;

                # # Method 2
                # for row in curs:
                #     # arr.append(f"{row}")  # This would probably be like above;
                #     resultList.append(row)
                #     # This should create multidimensional list;
                #     # Each field is a separate list item;

                # # for (first_name, last_name) in cur:
                # #     print(f"First Name: {first_name}, Last Name: {last_name}")


        cc = self.pool.connection_count
        ps = self.pool.pool_size
        logger.info(f"connection count: {cc}, pool size: {ps}")

        pool_connect.close()

                # # cc = self.pool.connection_count
                # # ps = self.pool.pool_size
                # # gLib.uwsgi_log(f"connection count2: {cc}")
                # # gLib.uwsgi_log(f"pool size2: {ps}")

                # # for x in range(10000000):
                # #     y = "hello"

                # logger.info(f"resultList: {resultList}")
                # # self.doDisconnect()
                # return resultList


        return curs

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

        # logger.info("Begin Connect")

        # if self.pool is not None:
        #     gLib.uwsgi_log("Already Connected")
        #     return;

        pool_conf = self.getConfig()

        logger.info("Connecting")
        
        try:
            # logger.info("begin try connect")
                
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

            # logger.info("end try connect")

        except mariadb.Error as e:
            # print(f"Error connecting to mariadb: {e}")
            return e

        finally:
            logger.info("Connected")

