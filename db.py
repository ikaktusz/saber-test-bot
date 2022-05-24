import sqlite3


conn = sqlite3.connect("authenticated.db")
cursor = conn.cursor()


def user_exists(user_id):
    user_id = int(user_id)
    cursor.execute(f"SELECT user_id FROM auths WHERE user_id=({user_id})")
    return cursor.fetchone()


def login(user_id):
    user_id = int(user_id)
    cursor.execute(f"INSERT INTO auths values ({user_id})")
    conn.commit()


def logout(user_id) -> None:
    user_id = int(user_id)
    cursor.execute(f"DELETE FROM auths WHERE user_id=({user_id})")
    conn.commit()


def _init_db():
    cursor.executescript("create table auths(user_id integer primary key);")
    conn.commit()


def check_db_exists():
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='auths'"
        )
    table_exists = cursor.fetchall()
    if table_exists:
        return
    _init_db()


check_db_exists()
