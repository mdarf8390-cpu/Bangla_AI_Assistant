from automation.browser import BrowserAutomation
from automation.skills.base import BaseSkill
import webbrowser


class GoogleSkill(BaseSkill):

    def __init__(self):

        super().__init__()

        self.browser = BrowserAutomation()


    def open(self):

        webbrowser.open(
            "https://www.google.com"
        )

        return True


    def search(self, query):

        self.browser.open_google(query)

        return True