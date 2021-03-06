import sqlite3


from numpy import insert
from requests import post

exercises_db_file_location = "database/exercises.db"
users_db_file_location = "database/users.db"
foro_db_file_location = "database/foro.db"

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

def register_user(email, name, last_name, password, rol):
    _conn = sqlite3.connect(users_db_file_location)
    _c = _conn.cursor()
    print("INSERT INTO users(email, first_name, last_name, password,rol) VALUES('{}','{}','{}','{}','{}')".format(email, name, last_name, password,rol))

    _c.execute("INSERT INTO users(email, first_name, last_name, password,rol) VALUES('{}','{}','{}','{}','{}')".format(email, name, last_name, password,rol))
    _conn.commit()
    _conn.close()

def get_hilo(idHilo, first):
    
    try:
        _conn = sqlite3.connect(foro_db_file_location)
        _c = _conn.cursor()
        _c.execute("ATTACH DATABASE ? as users;",(users_db_file_location,))
        _c.execute("SELECT usuario, mensaje, fechaHora, postId, hilo, rol, first_name, last_name FROM post INNER JOIN users.users on usuario = email WHERE hilo = '{}' AND first = {};".format(str(idHilo), str(first)))
    except Exception as e:
        print("illegal char s      :"+str(e))
        return 0
    result = [x for x in _c.fetchall()]

    _conn.close()

    return result

def get_hilos():
    

    _conn = sqlite3.connect(foro_db_file_location)
    _c = _conn.cursor()

    _c.execute("ATTACH DATABASE ? as users;",(users_db_file_location,))
    _c.execute("SELECT usuario, mensaje, fechaHora, postId, hilo, rol, first_name, last_name FROM main.post inner join users.users on usuario = email WHERE first = 1 ORDER BY fechaHora;")

    result = [x for x in _c.fetchall()]
    print(result)
    _conn.close()

    return result


def get_user_data(user_email):
    _conn = sqlite3.connect(users_db_file_location)
    _c = _conn.cursor()

    _c.execute("SELECT first_name, last_name, password FROM users WHERE email = '{}';".format(user_email))
    result = [x for x in _c.fetchall()]

    _conn.close()

    if result:
        return result[0]
    else:
        return None

def crear_post(text, name,hilo):
    _conn = sqlite3.connect(foro_db_file_location)
    _c = _conn.cursor()
    _c.execute("select hilo from post GROUP BY hilo ORDER BY fechaHora DESC LIMIT 1;")
    result = [x for x in _c.fetchall()]
    print(result)
    if hilo==-1:
        if bool(result):
            id = int(result[0][0])+1
        else:
            id = 0
        _c.execute("insert into post(usuario,mensaje,fechaHora,hilo,first) VALUES('{}','{}',DATETIME(),'{}',1);".format(name,text,id))
    else:
        _c.execute("insert into post(usuario,mensaje,fechaHora,hilo,first) VALUES('{}','{}',DATETIME(),'{}',0);".format(name,text,hilo))

    _conn.commit()
    _conn.close()

# insert into post(usuario,mensaje,fechaHora,hilo) VALUES("usuario","mensaje",DATETIME(),1);
# alter table post drop column postId;
# alter table post add column postId INTEGER AUTOINCREMENT;


# CREATE TABLE post (
#                             usuario TEXT NOT NULL,
#                             mensaje TEXT NOT NULL,
#                             fechaHora TEXT NOT NULL,
#                             postId INTEGER PRIMARY KEY AUTOINCREMENT,
#                             hilo integer not null
# );

# insert into post(usuario,mensaje,fechaHora,hilo) VALUES("I??igo","El ligonleyen es el mejor juego?",DATETIME(),2);
# insert into post(usuario,mensaje,fechaHora,hilo) VALUES("Riot Games","Si, evidentemente. Su contenido es sublime, ofrece interminables horas de diversion y una amplia variedad de modos de juego.",DATETIME(),2);
