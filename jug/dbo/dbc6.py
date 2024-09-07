
class Dbc():

    def __init__(self):
        self.db = False
        pass


    def commit_transaction(self):
        self.db.commit()


    def doDisconnect(self):

        if self.db:
            self.db.close
            # self.db = False


        # When to close connection??



    def doQuery(self):

        # https://mariadb.com/docs/server/connect/programming-languages/python/example/
        self.doConnect()
          # Create connection pool;


        # query = "SELECT * FROM ARTICLES $status_date ORDER BY DATETIME DESC LIMIT $start, $rows"
        # query = "SELECT * FROM ARTICLES LIMIT 1"
        # query = "SELECT * FROM ARTICLES"
        # query = "'SELECT first_name,last_name FROM employees WHERE first_name=?', (some_name,)"

        # establish pool connection
        pool_connect = self.db.get_connection()

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


        self.doDisconnect()
        return resultList



    #def static function doConnect($sphinx = false) {
    def doConnect(self):

        # if self.pool:
        #     return;
            
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