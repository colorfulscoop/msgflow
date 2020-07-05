class MyApp:
    def __init__(self, config):
        """"""

    def handle(self, message):
        res = f"{message.text} => Hi, how are you?"
        message.respond(res)
