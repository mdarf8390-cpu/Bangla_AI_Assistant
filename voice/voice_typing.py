# voice/voice_typing.py

import pyautogui


class VoiceTyping:


    def type_text(self, text):

        if not text:
            return False


        pyautogui.write(
            text,
            interval=0.03
        )


        return True