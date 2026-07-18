from core.command_parser import CommandParser
from core.planner import Planner
from core.context import ContextManager
from plugins.plugin_manager import PluginManager


class Brain:

    def __init__(self):

        self.parser = CommandParser()

        self.plugins = PluginManager()

        self.planner = Planner()

        self.context = ContextManager()


    def think(self, text):

        # -------------------------
        # Parse Command
        # -------------------------

        command = self.parser.parse(text)

        if command is None:

            command = {
                "action": "chat",
                "text": text
            }


        # -------------------------
        # Context Commands
        # -------------------------

        if (
            "বন্ধ" in text
            or "close" in text.lower()
            or "stop" in text.lower()
        ):

            last_action = self.context.get(
                "last_action"
            )

            if last_action == "youtube":

                command = {
                    "action": "youtube_close"
                }


        print(f"[Brain] Command : {command}")

        action = command.get("action")


        # -------------------------
        # Remember last action
        # -------------------------

        if action in [

            "youtube",

            "google",

            "chrome",

            "search",

            "write",

            "open"

        ]:

            self.context.update(command)


        # -------------------------
        # Planner
        # -------------------------

        if action != "chat":

            return self.planner.create_plan(command)


        # -------------------------
        # AI Chat
        # -------------------------

        answer = self.plugins.ask(

            command.get(
                "text",
                text
            )

        )


        return self.planner.create_plan(

            {

                "action": "chat",

                "answer": answer

            }

        )