# ai/decision.py

class Decision:

    def __init__(
        self,
        action=None,
        app=None,
        query="",
        text="",
        target=None
    ):

        self.action = action
        self.app = app
        self.query = query
        self.text = text
        self.target = target


    def to_dict(self):

        return {
            "action": self.action,
            "app": self.app,
            "query": self.query,
            "text": self.text,
            "target": self.target
        }


    def __str__(self):

        return str(self.to_dict())