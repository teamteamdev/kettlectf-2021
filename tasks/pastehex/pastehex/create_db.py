import sqlite3
from sys import argv
from os import remove

state_dir = argv[1]
path = state_dir + "/pastehex.db"
remove(path)

db = sqlite3.connect(path)
c = db.cursor()
c.execute(
    """
    CREATE TABLE IF NOT EXISTS "posts" (
        "id"	INTEGER NOT NULL UNIQUE,
        "post"	TEXT,
        "is_admin"	INTEGER NOT NULL DEFAULT 0,
        PRIMARY KEY("id" AUTOINCREMENT)
        );
        """
        )

c.execute(
    """
    INSERT INTO posts (id, post, is_admin) VALUES (0, 'Flag is here: https://bit.ly/3vLmsBl', 1)
    """
)

db.commit()
db.close()