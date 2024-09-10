import logging
logger = logging.getLogger(__name__)

import random
from jug.dbo import dbc
from jug.lib import gLib


class HomeDb():

    def __init__(self):
        pass


    def doHomeDb(self):

        try:
            dbo = dbc.Dbc()
            dbo.doConnect()

            query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"

            # result = dbo.doQuery()[0][4]
            logger.info('#1 query')
            # gLib.uwsgi_log("#1 query")
            # print("---#1 query")

            db_result = dbo.doQuery(query)
            # gLib.uwsgi_log("---#2 query")
            # db_result = dbo.doQuery(query)
            # gLib.uwsgi_log("---#3 query")
            # db_result = dbo.doQuery(query)
            # gLib.uwsgi_log("---#4 query")
            # db_result = dbo.doQuery(query)
            # gLib.uwsgi_log("---#5 query")
            # db_result = dbo.doQuery(query)
            # gLib.uwsgi_log("---#6 query")
            # db_result = dbo.doQuery(query)

            # r_index = random.randrange(len(db_result))
            result = db_result[ random.randrange( len(db_result) ) ]

        except Exception as e:
            # print(f"Error committing transaction: {e}")
            return [["bad db connection", e]]
        finally:
            dbo.doDisconnect()
            pass

        logger.info('return result')
        return result


    def doStart(self):
        return self.doHomeDb()

