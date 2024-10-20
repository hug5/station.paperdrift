class G():

    db = {}
        # un
        # pw
        # host
        # port
        # database

    api = {}
        # weatherAPI_key

    site = {}
        # name
        # tagline
        # baseUrl

    debug = False

    # Call at start to reset varables;
    @staticmethod
    def reset():
        G.db.clear()
        G.api.clear()
        G.site.clear()
        G.debug = False


# Problem with this format is that access is verbose;
# Have to do: G["db]["un"]
# Or worse: G.get("db", {}).get("un")

# G = {
#     "db" : {
#         "un" : None,
#         "pw" : None,
#         "host" : None,
#         "port" : None,
#         "database" : None
#     },

#     "weatherAPI_key" : None
# }