# ai/context.py

class ContextManager:

    def __init__(self):
        self.context = {
            "user": {},
            "conversation": [],
            "current_task": None,
            "last_action": None
        }


    def update(self, key, value):
        """
        Update context data
        """
        self.context[key] = value


    def get(self, key, default=None):
        """
        Get context data
        """
        return self.context.get(key, default)


    def add_message(self, role, message):
        """
        Save conversation history
        """

        self.context["conversation"].append({
            "role": role,
            "message": message
        })


    def set_task(self, task):
        """
        Save current running task
        """

        self.context["current_task"] = task


    def set_last_action(self, action):
        """
        Save last executed action
        """

        self.context["last_action"] = action


    def clear(self):
        """
        Clear temporary context
        """

        self.context = {
            "user": {},
            "conversation": [],
            "current_task": None,
            "last_action": None
        }


    def show(self):
        """
        Debug context
        """

        return self.context