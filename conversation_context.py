class ConversationContext:
    def __init__(self, max_history_size=10):
        self.max_history_size = max_history_size
        self.history = []
        self.context = {}

    def add_to_history(self, user_input, bot_response):
        if len(self.history) >= self.max_history_size:
            self.history.pop(0)  # Remove the oldest entry
        self.history.append({"user_input": user_input, "bot_response": bot_response})

    def get_context(self):
        return self.context.copy()

    def update_context(self, new_context):
        self.context.update(new_context)
