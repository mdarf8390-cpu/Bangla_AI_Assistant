import webbrowser

from automation.skills.base import BaseSkill


class DiscordSkill(BaseSkill):

    def __init__(self):

        super().__init__()


    def open(self):

        webbrowser.open(
            "https://discord.com/app"
        )

        return True


    def write(self, text):

        if not self.activate("discord"):

            self.open()

        return self.type(text)


    def search(self, query):

        self.open()

        return self.type(query)


    def close(self):

        return self.window.close("discord")