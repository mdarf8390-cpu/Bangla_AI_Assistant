from automation.browser import BrowserAutomation
from automation.skills.base import BaseSkill
import webbrowser


class YouTubeSkill(BaseSkill):

    def __init__(self):

        super().__init__()

        self.browser = BrowserAutomation()


    def open(self):

        webbrowser.open(
            "https://www.youtube.com"
        )

        return True


    def search(self, query):

        self.browser.open_youtube(query)

        return True


    def close(self):

        return self.window.close("youtube")