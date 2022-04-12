import sqlite3

exercises_db_file_location = "database/exercises.db"
users_db_file_location = "database/users.db"

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

def register_user(email, name, last_name, password):
    _conn = sqlite3.connect(users_db_file_location)
    _c = _conn.cursor()
    print("INSERT INTO users(email, first_name, last_name, password) VALUES('{}','{}','{}','{}')".format(email, name, last_name, password))

    _c.execute("INSERT INTO users(email, first_name, last_name, password) VALUES('{}','{}','{}','{}')".format(email, name, last_name, password))
    _conn.commit()
    _conn.close()

def get_user_data(user_email):
    _conn = sqlite3.connect(users_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT first_name, last_name, password FROM users WHERE email = '{}';".format(user_email))
    result = [x for x in _c.fetchall()]

    _conn.close()

    return result[0]