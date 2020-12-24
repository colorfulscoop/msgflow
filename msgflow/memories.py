class ConversationMemory:
    def __init__(self, max_history=None):
        self._max_history = max_history
        self._context = dict()

    def add(self, key, msg):
        ctx = self._context.get(key, []) + [msg]

        if self._max_history and len(ctx) > self._max_history:
            ctx = ctx[len(ctx) - self._max_history :]

        self._context[key] = ctx

    def get(self, key):
        return self._context.get(key, [])
