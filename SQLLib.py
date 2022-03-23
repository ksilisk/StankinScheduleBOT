import sqlite3

con = sqlite3.connect('usersDB.db', check_same_thread=False)
cur = con.cursor()


def get_state(user_id):
    return cur.execute("SELECT state FROM users WHERE id = ?", (user_id,)).fetchone()[0]


def add_user(user_id):
    cur.execute("INSERT OR REPLACE INTO users (id) VALUES (?)", (user_id,))
    con.commit()


def set_state(user_id, state):
    cur.execute("UPDATE users SET state = ? WHERE id = ?", (state, user_id))
    con.commit()


def get_groups(user_id):
    groups = cur.execute("SELECT groups FROM users WHERE id = ?", (user_id,)).fetchone()[0]
    return groups.split(' ')


def add_group(user_id, group):
    groups = get_groups(user_id) + ' ' + group
    cur.execute("UPDATE users SET groups = ?, groups_count = groups_count + 1 WHERE id = ?", (groups, user_id))
    con.commit()


def get_groups_count(user_id):
    return cur.execute("SELECT groups_count FROM users WHERE id = ?", (user_id,)).fetchone()[0]
