from automation.browser import BrowserAutomation

from automation.skills.youtube import YouTubeSkill
from automation.skills.google import GoogleSkill
from automation.skills.notepad import NotepadSkill
from automation.skills.vscode import VSCodeSkill
from automation.skills.whatsapp import WhatsAppSkill
from automation.skills.telegram import TelegramSkill
from automation.skills.discord import DiscordSkill
from automation.skills.spotify import SpotifySkill

from services.window import WindowService
from services.keyboard import KeyboardService
from services.mouse import MouseService
from services.clipboard import ClipboardService


class AutomationEngine:

    def __init__(self):

        # Core Services
        self.browser = BrowserAutomation()

        self.window = WindowService()

        self.keyboard = KeyboardService()

        self.mouse = MouseService()

        self.clipboard = ClipboardService()

        # Skill Registry
        self.skills = {

         "youtube": YouTubeSkill(),

         "google": GoogleSkill(),

         "notepad": NotepadSkill(),

         "vscode": VSCodeSkill(),

         "whatsapp": WhatsAppSkill(),

         "telegram": TelegramSkill(),

         "discord": DiscordSkill(),

         "spotify": SpotifySkill()

        }


    def execute(self, command):

        action = command.get("action")

        app = command.get("app")


        # ==========================================
        # Skill System
        # ==========================================

        if app in self.skills:

            skill = self.skills[app]

            if action == "open":

                if hasattr(skill, "open"):

                    return skill.open()


            elif action == "search":

                if hasattr(skill, "search"):

                    return skill.search(
                        command.get("query", "")
                    )


            elif action == "write":

                if hasattr(skill, "write"):

                    return skill.write(
                        command.get("text", "")
                    )


            elif action == "activate":

                if hasattr(skill, "activate"):

                    return skill.activate()


            elif action == "close":

                if hasattr(skill, "close"):

                    return skill.close()

            return False


        # ==========================================
        # Legacy Browser Commands
        # ==========================================

        if action == "youtube":

            self.browser.open_youtube(
                command.get("query", "")
            )

            return True


        if action == "google":

            self.browser.open_google(
                command.get("query", "")
            )

            return True


        if action == "chrome":

            self.browser.open_chrome()

            return True


        # ==========================================
        # Generic Write
        # ==========================================

        if action == "write":

            text = command.get("text", "")

            target = command.get("target")


            if len(text) < 150:

                return self.keyboard.type(
                    text=text,
                    target=target
                )


            return self.clipboard.paste_text(
                text=text,
                target=target
            )


        # ==========================================
        # Window Control
        # ==========================================

        if action == "activate":

            return self.window.activate(
                command.get("target")
            )


        if action == "close":

            return self.window.close(
                command.get("target")
            )


        return False
