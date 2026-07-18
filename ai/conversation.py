# ai/conversation.py

from collections import deque
from datetime import datetime


class ConversationMemory:

    def __init__(self, max_history=50):

        self.max_history = max_history

        self.history = deque(maxlen=max_history)

        self.last_command = None
        self.last_app = None
        self.last_action = None
        self.last_query = None


    def remember(self, command: dict):

        if not command:
            return

        self.last_command = command

        self.last_action = command.get("action")
        self.last_app = command.get("app")
        self.last_query = command.get("query")

        self.history.append({

            "time": datetime.now(),

            "command": command

        })


    def get_last_app(self):

        return self.last_app


    def get_last_action(self):

        return self.last_action


    def get_last_query(self):

        return self.last_query


    def get_last_command(self):

        return self.last_command


    def get_history(self):

        return list(self.history)


    def clear(self):

        self.history.clear()

        self.last_command = None
        self.last_app = None
        self.last_action = None
        self.last_query = None


    def resolve_context(self, command):

        """
        যদি app না থাকে,
        আগের app ব্যবহার করবে।
        """

        if command.get("app") is None:

            command["app"] = self.last_app

        return command