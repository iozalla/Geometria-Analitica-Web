import sqlite3

exercises_db_file_location = "database/exercises.db"

def get_questions():
    _conn = sqlite3.connect(exercises_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT * FROM questions;")
    result = [x for x in _c.fetchall()]

    _conn.close()

    return result


def get_tests():
    _conn = sqlite3.connect(exercises_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT * FROM tests;")
    result = [x for x in _c.fetchall()]

    _conn.close()

    return result

