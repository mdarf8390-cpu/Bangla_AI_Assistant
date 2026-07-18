# ai/reasoner.py

from .decision import Decision


class Reasoner:


    def analyze(self, intent, data=None):

        data = data or {}

        if intent == "youtube":

            return Decision(
                action="open",
                app="youtube",
                query=data.get("query", "")
            )


        if intent == "google":

            return Decision(
                action="search",
                app="google",
                query=data.get("query", "")
            )


        if intent == "notepad":

            return Decision(
                action="open",
                app="notepad"
            )


        if intent == "vscode":

            return Decision(
                action="open",
                app="vscode"
            )


        return Decision(
            action="unknown"
        )