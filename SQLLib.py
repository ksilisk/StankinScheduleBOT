import sqlite3

con = sqlite3.connect('usersDB.db', check_same_thread=False)
cur = con.cursor()


def add_user(user_id):
    cur.execute("INSERT INTO users (Id) VALUES (?)", (user_id, ))
    con.commit()


def del_user(user_id):
    cur.execute("DELETE FROM users WHERE id = ?", (user_id,))
    con.commit()


def get_state(user_id):
    return cur.execute("SELECT state FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def add_user(user_id):
    cur.execute("INSERT OR REPLACE INTO users (id) VALUES (?)", (user_id,))
    con.commit()


def add_time_send(user_id, time):
    cur.execute("UPDATE users SET time_send = ? WHERE id = ?", (time, user_id))
    con.commit()


def get_time_send(user_id):
    return cur.execute("SELECT time_send FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def add_schedule_id(user_id, mes_id):
    cur.execute("UPDATE users SET schedule_id = ? WHERE id = ?", (mes_id, user_id))
    con.commit()


def get_schedule_id(user_id):
    return cur.execute("SELECT schedule_id FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def set_state(user_id, state):
    cur.execute("UPDATE users SET state = ? WHERE id = ?", (state, user_id))
    con.commit()


def set_groups(user_id, text):
    cur.execute("UPDATE users SET groups = ? WHERE id = ?", (text, user_id))
    con.commit()


def get_groups(user_id):
    return cur.execute("SELECT groups FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def add_group(user_id, group):
    if get_groups_count(user_id) == 0:
        cur.execute("UPDATE users SET groups = ?, groups_count = groups_count + 1 WHERE id = ?", (group, user_id))
    else:
        cur.execute("UPDATE users SET groups = groups || ?, groups_count = groups_count + 1 WHERE id = ?", (' ' + group, user_id))
    con.commit()


def check_user(user_id):
    if len(cur.execute("SELECT * FROM users WHERE id = ?", (user_id,)).fetchall()) == 1:
        return True
    return False


def get_groups_count(user_id):
    return cur.execute("SELECT groups_count FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def get_users_with_time():
    return cur.execute("SELECT id, time_send FROM users WHERE time_send IS NOT NULL").fetchall()