import subprocess
import time

from automation.skills.base import BaseSkill


class VSCodeSkill(BaseSkill):

    def open(self):

        if self.activate("visual studio code"):

            return True

        subprocess.Popen("code")

        time.sleep(3)

        return self.activate("visual studio code")


    def write(self, text):

        if not self.open():

            return False

        return self.type(text)