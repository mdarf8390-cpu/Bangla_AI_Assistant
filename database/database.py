import sqlite3
from pathlib import Path
from datetime import datetime


class Database:

    def __init__(self):

        self.db_folder = Path("database")
        self.db_folder.mkdir(exist_ok=True)

        self.db_path = self.db_folder / "ayesha_memory.db"

        self.conn = sqlite3.connect(
            self.db_path,
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()


    def create_tables(self):

        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS memories(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            category TEXT,

            key TEXT,

            value TEXT,

            importance INTEGER DEFAULT 1,

            created_at TEXT

        )

        """)


        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS conversation(

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            role TEXT,

            message TEXT,

            created_at TEXT

        )

        """)


        self.cursor.execute("""

        CREATE TABLE IF NOT EXISTS settings(

            key TEXT PRIMARY KEY,

            value TEXT

        )

        """)

        self.conn.commit()


    # -----------------------
    # Memory
    # -----------------------

    def save_memory(
        self,
        category,
        key,
        value,
        importance=1
    ):

        self.cursor.execute(

            """

            INSERT INTO memories

            (category,key,value,importance,created_at)

            VALUES(?,?,?,?,?)

            """,

            (

                category,

                key,

                value,

                importance,

                datetime.now().isoformat()

            )

        )

        self.conn.commit()


    def get_memory(self,key):

        self.cursor.execute(

            "SELECT value FROM memories WHERE key=? ORDER BY id DESC LIMIT 1",

            (key,)

        )

        row=self.cursor.fetchone()

        if row:

            return row[0]

        return None


    # -----------------------
    # Conversation
    # -----------------------

    def save_chat(self,role,message):

        self.cursor.execute(

            """

            INSERT INTO conversation

            (role,message,created_at)

            VALUES(?,?,?)

            """,

            (

                role,

                message,

                datetime.now().isoformat()

            )

        )

        self.conn.commit()


    def last_chat(self,limit=20):

        self.cursor.execute(

            """

            SELECT role,message

            FROM conversation

            ORDER BY id DESC

            LIMIT ?

            """,

            (limit,)

        )

        return self.cursor.fetchall()


    # -----------------------
    # Settings
    # -----------------------

    def set_setting(self,key,value):

        self.cursor.execute(

            """

            INSERT OR REPLACE INTO settings

            VALUES(?,?)

            """,

            (

                key,

                value

            )

        )

        self.conn.commit()


    def get_setting(self,key):

        self.cursor.execute(

            "SELECT value FROM settings WHERE key=?",

            (key,)

        )

        row=self.cursor.fetchone()

        if row:

            return row[0]

        return None


if __name__ == "__main__":

    db=Database()

    db.save_memory(

        "profile",

        "name",

        "Arfat",

        5

    )

    print(db.get_memory("name"))