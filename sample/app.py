class MyApp:
    def __init__(self, config):
        """"""

    def handle(self, message):
        res = f'As you say "{message.text}", how are you?'
        message.respond(res)
