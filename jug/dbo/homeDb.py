from jug.lib.logger import logger
import random
from jug.dbo import dbc

# from jug.lib.f import F


class HomeDb():

    def __init__(self):
        pass


    def doHomeDb(self):

        try:
            dbo = dbc.Dbc()
            dbo.doConnect()

            # query  = "SELECT ARTICLENO, HEADLINE, BLURB FROM ARTICLES"
            query  = "SELECT HEADLINE FROM ARTICLES WHERE STATUS='N' AND TAGS='paperdrift'"

            # result = dbo.doQuery()[0][4]
            # logger.info('#1 query')
            # F.uwsgi_log("#1 query")
            # print("---#1 query")


            # #-------------------------------
            # db_result = dbo.doQuery(query)
            # # F.uwsgi_log("---#2 query")
            # # db_result = dbo.doQuery(query)
            # # F.uwsgi_log("---#3 query")
            # # db_result = dbo.doQuery(query)
            # # F.uwsgi_log("---#4 query")
            # # db_result = dbo.doQuery(query)
            # # F.uwsgi_log("---#5 query")
            # # db_result = dbo.doQuery(query)
            # # F.uwsgi_log("---#6 query")
            # # db_result = dbo.doQuery(query)

            # # r_index = random.randrange(len(db_result))
            # result = db_result[ random.randrange( len(db_result) ) ]
            # # for (first_name, last_name) in cur:
            # #     print(f"First Name: {first_name}, Last Name: {last_name}")
            # #-------------------------------

            # get back cursor
            curs = dbo.doQuery(query)
            # logger.info(f"curs: {curs}")  # this gives me a binary value;

            result_list = []

            # If 2 or more fields, do this way:
            # for (ARTICLENO, HEADLINE, BLURB) in curs:
            #     result_list.append( {"ARTICLENO":ARTICLENO, "HEADLINE" : HEADLINE, "BLURB": BLURB} )

            # Result is a list composed of dictionaries;
            # [
            #   {'ARTICLENO': 1002, 'HEADLINE': 'Gone with the dogs, in with the swines', 'BLURB': 'Lunar/Chinese New Year 2019, Year of the Pig'},
            #   {'ARTICLENO': 1004, 'HEADLINE': 'The Long Train Ride', 'BLURB': 'DPRK/US Hanoi Summit 2019'}, {'ARTICLENO': 1005, 'HEADLINE': 'Beauty is but a flower, which wrinkles will devour', 'BLURB': 'A poem by 16th century English playwright Thomas Nashe'},
            #   {'ARTICLENO': 1007, 'HEADLINE': 'Redefining Poverty Down', 'BLURB': 'Austerity for the poor, trickle up for the rich'}
            # ]

            # ....

            # If single field, do this way:
            for row in curs:
                result_list.append(row[0])
                # for (row) in curs: with or without ( ) doesn't matter
                # Returns values in a tuple; so have to extract the first value;
                # if do row:
                # [('Woolly rhino found preserved in Russian permafrost after 32,000 years',), ('Radar images capture snowman-shaped object tumbling past Earth',), ('DNA from 3,600-year-old cheese sequenced by scientists',)]
                # If do row[0], then will get:
                # ['Woolly rhino found preserved in Russian permafrost after 32,000 years', 'Radar images capture snowman-shaped object tumbling past Earth', 'DNA from 3,600-year-old cheese sequenced by scientists']
                # row[0] seems to extract the first tuple; and then append that to the list;



            logger.info(f"db_result: {result_list}")

            # IF obtaining a single field, then strangely the result is like this: wraps the headline like a row of tuples; notice there's always a comma at the end as if anticipating more;

            # If single field:
            # [
            #   {'HEADLINE': ('Woolly rhino found preserved in Russian permafrost after 32,000 years',)},
            #   {'HEADLINE': ('Radar images capture snowman-shaped object tumbling past Earth',)},
            #   {'HEADLINE': ('DNA from 3,600-year-old cheese sequenced by scientists',)}
            # ]

            # Or regardless of how I append it, it's something like:
            # [
            #   ('Woolly rhino found preserved in Russian permafrost after 32,000 years',),
            #   ('Radar images capture snowman-shaped object tumbling past Earth',),
            #   ('DNA from 3,600-year-old cheese sequenced by scientists',)
            # ]

            # Only appending like this will thus get rid of the strange formatting:
            # result_list.append(row[0])


            db_result = result_list[ random.randrange( len(result_list) ) ]
            logger.info(f"db_result: {db_result}")
            # Result is a single dictionary:
            # {'ARTICLENO': 1008, 'HEADLINE': "It's On! Fox News' Trish Regan vs. CGTN's Liu Xin", 'BLURB': "Liu accepts Regan's invitation to a live US/China trade debate on Fox"}


            #--------
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
        return [db_result]
            # return as list, not string; will combine with other news list later;
