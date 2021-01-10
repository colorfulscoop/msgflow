class DialogMemory:
    def __init__(self, max_history=None):
        self._max_history = max_history
        self._context = dict()

    def add(self, dialog_id, msg):
        ctx = self._context.get(dialog_id, []) + [msg]

        if self._max_history and len(ctx) > self._max_history:
            ctx = ctx[len(ctx) - self._max_history :]

        self._context[dialog_id] = ctx

    def get(self, dialog_id):
        return self._context.get(dialog_id, [])

    def clear(self, dialog_id):
        if dialog_id in self._context:
            self._context[dialog_id] = []
