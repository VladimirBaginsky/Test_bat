import sqlite3 as sq

def reg_user(login="user", password=1, scores=0):
    if login == "": login = "user"
    if password == "": password = 0

    with sq.connect("snake.db") as con:
        cur = con.cursor()

        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            login TEXT NOT NULL, 
            password TEXT NOT NULL, 
            scores INTEGER 
            )""")

        cur.execute(f"SELECT login FROM users WHERE login = '{login}'")
        row = cur.fetchone()
        if row is None:
            cur.execute("INSERT INTO users VALUES (?, ?, ?)",(login, password, scores))
            con.commit()
            print("Пользователь ", login, " успешно зарегестрирован!")
            return True
        else:
            cur.execute(f"SELECT password FROM users WHERE login = '{login}'")
            row = cur.fetchone()
            if row[0] == password:
                print("Пароль принят!")
                return True
            else:
                print("Неверный пароль!")
                return False


def read_scores(login):

    with sq.connect("snake.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT login FROM users WHERE login = '{login}'")
        if not cur.fetchone() is None:
            cur.execute(f"SELECT scores FROM users WHERE login = '{login}'")
            row = cur.fetchone()
            return row[0]

def edit_scores(login, scores=0):

    with sq.connect("snake.db") as con:
        cur = con.cursor()
        cur.execute(f"SELECT login FROM users WHERE login = '{login}'")
        if not cur.fetchone() is None:
            cur.execute(f"UPDATE users SET scores= {scores} WHERE login = '{login}'")

def get_best():

    with sq.connect("snake.db") as con:
        cur = con.cursor()
        cur.execute("SELECT * FROM users WHERE scores > 0 ORDER BY scores DESC LIMIT 5")
        res = cur.fetchall()
        return res
