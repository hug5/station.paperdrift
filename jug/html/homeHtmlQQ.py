# result = "<!doctype html> \
# <head></head> \
# <html> \
# <body> \
# \
#     <p>hello {{msg[0]}}</p> \
#     <p>The weather is {{msg[1]}}</p> \
#     <p>The mood today is {{msg[2]}}</p> \
#     <p>User agent is: {{user_agent}}</p> \
#     <p>Who: {{ dog.name, dog.age, dog.location }}</p> \
#     <p>Today is: {{dog.dayName}}, {{dog.now}}</p> \
#     <p>My calculation: {{dog.mult(2)}}</p> \
# \
# </body> \
# </html>"


class HomeHtml:

    def __init__(self):
        pass

    def doHtml(Obj1):

        html = "<p>hello " +  Obj1.name + "</p>"
        html += "<p>The weather is {{msg[1]}}</p>"
        # <p>The mood today is {{msg[2]}}</p> \
        # <p>User agent is: {{user_agent}}</p> \
        # <p>Who: {{ dog.name, dog.age, dog.location }}</p> \
        # <p>Today is: {{dog.dayName}}, {{dog.now}}</p> \
        # <p>My calculation: {{dog.mult(2)}}</p>"
        return html



# class Obj1:
#     name = "Bobby"
#     age = 21
#     location = "Miami"
#     dayName = dayNameList[dayNameIndex]
#     now = datetime.now()
#     def mult(arg):
#         return arg*3

