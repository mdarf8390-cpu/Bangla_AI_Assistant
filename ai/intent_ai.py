# ai/intent_ai.py


class IntentAI:

    def __init__(self):

        self.actions = [

            "open",
            "close",
            "search",
            "write",
            "play"

        ]

        self.apps = [

            "youtube",
            "google",
            "chrome",
            "vscode",
            "notepad",
            "telegram",
            "discord",
            "spotify",
            "whatsapp"

        ]


    def detect(self, text):

        command = {

            "action": None,
            "app": None,
            "query": "",
            "text": "",
            "target": None

        }

        words = text.split()

        for word in words:

            if word in self.actions:

                command["action"] = word

            if word in self.apps:

                command["app"] = word


        if command["action"] == "search":

            skip = set(self.actions + self.apps)

            command["query"] = " ".join(

                w for w in words

                if w not in skip

            )


        elif command["action"] == "write":

            skip = set(self.actions + self.apps)

            command["text"] = " ".join(

                w for w in words

                if w not in skip

            )

        return command