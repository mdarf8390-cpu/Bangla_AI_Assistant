class CommandParser:


    def clean_query(self, query):

        remove_words = [
            "চালাও",
            "খুঁজে দাও",
            "খুঁজে",
            "দাও",
            "search",
            "play",
            "open",
            "এ",
            "তে",
            "এটা"
        ]


        for word in remove_words:

            query = query.replace(word, "")


        return query.strip()



    def parse(self, text):

        text = text.lower().strip()


        # remove assistant name
        text = text.replace("ayesha", "")
        text = text.replace("এয়েশা", "")

        text = text.strip()



        # YouTube

        if "youtube" in text or "ইউটিউব" in text:

            query = text

            query = query.replace(
                "youtube",
                ""
            )

            query = query.replace(
                "ইউটিউব",
                ""
            )


            return {
                "action": "youtube",
                "query": self.clean_query(query)
            }



        # Google

        if "google" in text or "গুগল" in text:

            query = text

            query = query.replace(
                "google",
                ""
            )

            query = query.replace(
                "গুগল",
                ""
            )


            return {
                "action": "google",
                "query": self.clean_query(query)
            }



        # Chrome

        if (
            "chrome" in text
            or "ক্রোম" in text
            or "browser" in text
        ):

            return {
                "action": "chrome"
            }



        return {
            "action": "chat",
            "text": text
        }