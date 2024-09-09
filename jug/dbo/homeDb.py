from jug.dbo import dbc
import random
from jug.lib import gLib


class HomeDb():

    def __init__(self):
        pass


    def doHomeDb(self):

        try:

            # dbc = False
            dbo = dbc.Dbc()
            dbo.doConnect()

            # result = dbo.doQuery()[0][4]
            gLib.uwsgi_log("---#1 query")
            result = dbo.doQuery()
            gLib.uwsgi_log("---#2 query")
            result = dbo.doQuery()
            gLib.uwsgi_log("---#3 query")
            result = dbo.doQuery()
            gLib.uwsgi_log("---#4 query")
            result = dbo.doQuery()
            gLib.uwsgi_log("---#5 query")
            result = dbo.doQuery()
            gLib.uwsgi_log("---#6 query")

            db_result = dbo.doQuery()

            max = len(db_result)
            r_index = random.randrange(0, max)
            result = db_result[r_index]

            # result = db_result


            # return gLib.hesc(dbc)
        except Exception as e:
            # print(f"Error committing transaction: {e}")
            return [["bad db connection", e]]
        finally:
            dbo.doDisconnect()
            pass


        return result


    def doStart(self):
        return self.doHomeDb()

