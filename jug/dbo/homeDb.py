# from jug.lib.logger import logger
# import logging
# logger = logging.getLogger(__name__)

import random
from jug.dbo import dbc
from jug.lib.logger import logger

# from jug.lib import gLib


class HomeDb():

    def __init__(self):
        pass


    def doHomeDb(self):

        try:
            dbo = dbc.Dbc()
            dbo.doConnect()

            # query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"
            query  = "SELECT ARTICLENO, HEADLINE FROM ARTICLES WHERE STATUS='N' AND TAGS='paperdrift'"

            # result = dbo.doQuery()[0][4]
            # logger.info('#1 query')
            # gLib.uwsgi_log("#1 query")
            # print("---#1 query")


            # #-------------------------------
            # db_result = dbo.doQuery(query)
            # # gLib.uwsgi_log("---#2 query")
            # # db_result = dbo.doQuery(query)
            # # gLib.uwsgi_log("---#3 query")
            # # db_result = dbo.doQuery(query)
            # # gLib.uwsgi_log("---#4 query")
            # # db_result = dbo.doQuery(query)
            # # gLib.uwsgi_log("---#5 query")
            # # db_result = dbo.doQuery(query)
            # # gLib.uwsgi_log("---#6 query")
            # # db_result = dbo.doQuery(query)

            # # r_index = random.randrange(len(db_result))
            # result = db_result[ random.randrange( len(db_result) ) ]
            # # for (first_name, last_name) in cur:
            # #     print(f"First Name: {first_name}, Last Name: {last_name}")
            # #-------------------------------

            # get back cursor
            curs = dbo.doQuery(query)

            result_list = []

            for (ARTICLENO, HEADLINE) in curs:
                result_list.append(HEADLINE)
                # db_result.append( {"HEADLINE" : HEADLINE} )
                # list composed of a dictionary;


            db_result = result_list[ random.randrange( len(result_list) ) ]
            logger.info(f"db_result: {db_result}")


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



        except Exception as e:
            # print(f"Error committing transaction: {e}")
            return [["bad db connection", e]]
        finally:
            dbo.doDisconnect()
            pass

        # logger.info('return result')
        return db_result


    def doStart(self):
        return self.doHomeDb()

