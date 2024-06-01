
class DomHtml:

    def __init__(self):
        self.html = ''

    def doHtml(self, arg):

        self.html = "\
        <p>hello " +  Obj1.name + "</p>                       \
        <p>The weather is {{msg[1]}}</p>                      \
        <p>The mood today is {{msg[2]}}</p>                   \
        <p>User agent is: {{user_agent}}</p>                  \
        <p>Who: {{ dog.name, dog.age, dog.location }}</p>     \
        <p>Today is: {{dog.dayName}}, {{dog.now}}</p>         \
        <p>My calculation: {{dog.mult(2)}}</p>                \
        "

        return self.html

        # self.html = Obj1
         # + "hello"
        # return self.html
        # return arg + " " + "hello."
