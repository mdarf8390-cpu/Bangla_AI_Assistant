# voice/wake_word.py


class WakeWordDetector:


    def __init__(self):

        self.active = False


    def check(self, text):

        if not text:
            return None


        text = text.lower().strip()


        # Wake words
        wake_words = [
            "ayesha",
            "এশা",
            "আয়েশা",
            "আয়েশা"
        ]


        # Off words
        off_words = [
            "off",
            "অফ",
            "stop",
            "sleep",
            "ঘুমাও",
            "বন্ধ"
        ]


        if not self.active:


            for word in wake_words:

                if word in text:

                    self.active = True

                    return "activated"



        else:


            for word in off_words:

                if word in text:

                    self.active = False

                    return "deactivated"



        return None



    def is_active(self):

        return self.active