import mariadb


class Dbc():

    def __init__(self):
        self.db = False
        pass

    ## Notes:
      #
      # def static function getLastError()
      #     $result = self::$Db->error; # to get back the error message
      #     return $result;

      # def static function getLastInsertId()
      #     #NOTE1: returns the auto generated id used in last query
      #     # returns 0 if bad connection or no autoincrement was performed
      #     #NOTE2: The php docs seeem to be wrong; the function will return ANY new index
      #     #value that was inserted into an autugenerated field, whether that value was
      #     #manually specified or generated automatically by DB;
      #     $id = self::$Db->insert_id;
      #     return $id;

      # def static function getNumIndices($table)

      #     #show keys or index will return all indices used in table, not just the primary tables;
      #     #but we want only the primary index here;

      #     $query  = "SHOW KEYS FROM $table WHERE Key_name = 'PRIMARY'"; #can also use: "Show Indexes from $table"
      #     $result = self::doQuery($query); /# result will return 1 on successful sql operation;

      #     if (!$result) return false;
      #     return $result->num_rows; #return number of results, which is the number of indices in table

      # def static function rollback_transaction()
      #     self::$Db->rollback();
      # def start_transaction():
      #     self::doConnect();
      #     self::$Db->autocommit(false);


      # cur.execute("UPDATE test.accounts SET amount=(amount-?) WHERE email=?", (change, email))
      # cur.execute("INSERT INTO test.accounts(first_name, last_name, email, amount) \ VALUES (?, ?, ?, ?)", (first_name, last_name, email, amount))
      # self.db.commit()
      # self.db.rollback()
      # result = cursor.execute('SELECT * FROM myTable LIMIT 10')
      # rows = cursor.fetchall()

      #---------------------------

      ## Insert

      # While inserting rows, you may want to find the Primary Key of the last inserted row when it is generated, as with auto-incremented values.
      # You can retrieve this using the lastrowid() method on the cursor.


      # try:
      #     cursor.execute("some MariaDB query"))
      # except mariadb.Error as e:
      #     print(f"Error: {e}")




    def commit_transaction(self):
        self.Db.commit()


    def doDisconnect(self):

        if self.db:
            self.db.close
            self.db = False


        # When to close connection??



    def doQuery(self):

        # https://mariadb.com/docs/server/connect/programming-languages/python/example/
        self.doConnect()

        # query = "SELECT * FROM ARTICLES $status_date ORDER BY DATETIME DESC LIMIT $start, $rows"
        # query = "SELECT * FROM ARTICLES LIMIT 1"
        # query = "SELECT * FROM ARTICLES"
        query = "'SELECT first_name,last_name FROM employees WHERE first_name=?', (some_name,)"


        # instantiate the cursor
        curs = self.db.cursor()

        # https://mariadb-corporation.github.io/mariadb-connector-python/cursor.html
        curs.prepared = True

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

        return resultList



    #def static function doConnect($sphinx = false) {
    def doConnect(self):

        if self.db:
            return;

        # $host     = F::json("config-admin", "host");
        # $database = F::json("config-admin", "database");
        # $un       = F::json("config-admin", "un");
        # $pw       = F::json("config-admin", "pw");
        # self::$Db = new \mysqli($host, $un, $pw, $database);
        # self::$Db->set_charset("utf8");

        un = "inkon"
        pw = "J##Dd*(r9TZYKh$%"
        host = "localhost"   # default
        port = 3306
        database = "inkonDb"
        autocommit = False

        try:
            self.db = mariadb.connect(
                user = un,
                password = pw,
                # host = host,
                port = port,
                database = database,
                # protocol = "SOCKET",
                autocommit = autocommit
            )

            # return self.db

        except mariadb.Error as e:
            # print(f"Error connecting to mariadb: {e}")
            return e


