import mariadb


class Dbc():

    def __init__(self):
        self.db = False
        pass



    # def static function doQuery($query)

    #     self::doConnect();
    #     # run the query, return mysqli_result OBJECT, not simply the raw result
    #     $result = self::$Db->query($query);

    #     return $result;

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

    # def static function commit_transaction()
    #     self::$Db->commit();

    # def static function start_transaction()
    #     self::doConnect();
    #     self::$Db->autocommit(false);

    # def static function doDisconnect()
    #     #echo "d:" . time();
    #     if ( self::$Db ) {
    #         self::$Db->close();
    #         self::$Db = null;
    #     }


    #def static function doConnect($sphinx = false) {
    def doConnect(self):

        # if self.db:
        #     return;

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

            return self.db

        except mariadb.Error as e:
            print(f"Error connecting to mariadb: {e}")
            return False

# dbo = Dbc()
# result = dbo.doConnect()
# print(result)

