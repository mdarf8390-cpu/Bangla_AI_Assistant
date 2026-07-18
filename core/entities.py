class EntityExtractor:

    def extract(self, text):

        text = text.lower()

        entity = {

            "app": None,
            "query": None,
            "text": None,
            "contact": None

        }


        # -----------------------
        # Apps
        # -----------------------

        apps = {

            "youtube": ["youtube", "yt"],

            "google": ["google"],

            "whatsapp": ["whatsapp", "wa"],

            "vscode": ["vs code", "vscode", "code"],

            "notepad": ["notepad"]

        }


        for app, words in apps.items():

            for word in words:

                if word in text:

                    entity["app"] = app

                    break


        return entity