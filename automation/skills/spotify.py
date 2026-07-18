import webbrowser

from automation.skills.base import BaseSkill


class SpotifySkill(BaseSkill):

    def __init__(self):

        super().__init__()


    def open(self):

        webbrowser.open(
            "https://open.spotify.com"
        )

        return True


    def search(self, query):

        self.open()

        return self.type(query)


    def play(self, song):

        self.search(song)

        self.press("enter")

        return True


    def close(self):

        return self.window.close("spotify")