class CommandParser:

    def parse(self, text):

        txt = text.lower()


        # -----------------------
        # Search
        # -----------------------

        if "youtube" in txt:

            query = txt.replace("youtube", "")

            query = query.replace("চালাও", "")

            query = query.replace("search", "")

            query = query.strip()


            return {

                "action": "search",

                "app": "youtube",

                "query": query

            }


        if "google" in txt:

            query = txt.replace("google", "")

            query = query.replace("খুঁজে", "")

            query = query.replace("দাও", "")

            query = query.strip()


            return {

                "action": "search",

                "app": "google",

                "query": query

            }


        # -----------------------
        # Notepad
        # -----------------------

        if "notepad" in txt and "লিখ" in txt:

            message = txt.split("লিখ")[-1].strip()


            return {

                "action": "write",

                "app": "notepad",

                "text": message

            }


        # -----------------------
        # VS Code
        # -----------------------

        if ("vscode" in txt or "vs code" in txt) and "লিখ" in txt:

            message = txt.split("লিখ")[-1].strip()


            return {

                "action": "write",

                "app": "vscode",

                "text": message

            }


        return None