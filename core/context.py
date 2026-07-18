class ContextManager:


    def __init__(self):

        self.data = {
            "last_action": None,
            "last_query": None,
            "last_task": None
        }



    def update(self, action_data):

        self.data["last_action"] = action_data.get("action")

        self.data["last_query"] = action_data.get("query")



    def get(self, key):

        return self.data.get(key)



    def remember(self):

        return self.data