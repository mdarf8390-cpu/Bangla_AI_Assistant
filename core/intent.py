class IntentDetector:

    def __init__(self):
        self.browser_commands = {
            "youtube": [
                "youtube",
                "yt",
                "ইউটিউব"
            ],
            "google": [
                "google",
                "গুগল"
            ],
            "chrome": [
                "chrome",
                "browser",
                "ক্রোম"
            ]
        }

    def detect(self, text):

        text = text.lower().strip()
        words = text.split()

        # ---------- YouTube ----------
        if "youtube" in words:
            return "youtube"

        if "yt" in words:
            return "youtube"

        if "ইউটিউব" in text:
            return "youtube"

        # ---------- Google ----------
        if "google" in words:
            return "google"

        if "গুগল" in text:
            return "google"

        # ---------- Chrome ----------
        if "chrome" in words:
            return "chrome"

        if "browser" in words:
            return "chrome"

        if "ক্রোম" in text:
            return "chrome"

        # ---------- Default ----------
        return "chat"


if __name__ == "__main__":

    detector = IntentDetector()

    while True:

        text = input("You : ")

        if text.lower() == "exit":
            break

        print("Intent =", detector.detect(text))