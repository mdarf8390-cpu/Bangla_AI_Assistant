from automation.browser import BrowserAutomation
from automation.skills.base import BaseSkill
import webbrowser


class WhatsAppSkill(BaseSkill):

    def __init__(self):

        super().__init__()

        self.browser = BrowserAutomation()


    def open(self):

        webbrowser.open(
            "https://web.whatsapp.com"
        )

        return True


    def activate(self):

        return self.window.activate("whatsapp")