from database.database import Database


class Memory:

    def __init__(self):

        self.db = Database()

        self.short_memory = []

    # -----------------------------
    # Temporary Memory
    # -----------------------------

    def remember_temporarily(self, text):

        self.short_memory.append(text)

        if len(self.short_memory) > 20:
            self.short_memory.pop(0)

    # -----------------------------
    # Long Term Memory
    # -----------------------------

    def remember(
        self,
        category,
        key,
        value,
        importance=1
    ):

        self.db.save_memory(
            category,
            key,
            value,
            importance
        )

    # -----------------------------
    # Recall
    # -----------------------------

    def recall(self, key):

        return self.db.get_memory(key)

    # -----------------------------
    # Chat History
    # -----------------------------

    def save_chat(self, role, message):

        self.db.save_chat(role, message)

    def history(self):

        return self.db.last_chat()

    # -----------------------------
    # Settings
    # -----------------------------

    def set_setting(self, key, value):

        self.db.set_setting(key, value)

    def get_setting(self, key):

        return self.db.get_setting(key)


if __name__ == "__main__":

    memory = Memory()

    memory.remember(
        "profile",
        "favorite_game",
        "GTA V",
        5
    )

    print(memory.recall("favorite_game"))

    memory.save_chat(
        "user",
        "Hello Ayesha"
    )

    print(memory.history())