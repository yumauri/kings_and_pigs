import sqlite3


class Database:
    con: sqlite3.Connection

    def __init__(self):
        self.con = sqlite3.connect(
            "kings_and_pigs/database/db.sqlite",
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
        )
        sqlite3.register_adapter(bool, int)
        sqlite3.register_converter("BOOLEAN", lambda v: bool(int(v)))
        self.con.row_factory = sqlite3.Row

    def close(self):
        self.con.close()

    def get_top_scores(self):
        con = self.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT id, name, score, win
            FROM score
            ORDER BY score DESC, id ASC
            LIMIT 10
            """
        ).fetchall()
        return result

    def add_score(self, name, score, win):
        con = self.con
        cur = con.cursor()
        cur.execute(
            """
            INSERT INTO score(name, score, win)
            VALUES (?, ?, ?)
            """,
            (name, score, win),
        )
        con.commit()
        return cur.lastrowid

    def get_settings(self):
        con = self.con
        cur = con.cursor()
        result = cur.execute(
            """
            SELECT name, value
            FROM settings
            """
        ).fetchall()

        # transform to a dictionary
        settings = {}
        for row in result:
            settings[row["name"]] = row["value"]
        return settings

    def set_settings(self, settings):
        con = self.con
        cur = con.cursor()
        for name, value in settings.items():
            cur.execute(
                """
                UPDATE settings
                SET value = ?
                WHERE name = ?
                """,
                (value, name),
            )
            con.commit()
