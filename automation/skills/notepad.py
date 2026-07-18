import subprocess
import time

from automation.skills.base import BaseSkill


class NotepadSkill(BaseSkill):

    def open(self):

        if self.activate("notepad"):

            return True

        subprocess.Popen("notepad.exe")

        time.sleep(1)

        return self.activate("notepad")


    def write(self, text):

        if not self.open():

            return False

        return self.type(text)