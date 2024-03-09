import sqlite3, logging
from utils import date

conn = sqlite3.connect('database/database.db', check_same_thread=False)
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users
                  (name TEXT, username TEXT, user_id INTEGER PRIMARY KEY, date TEXT)
                ''')
cursor.execute('''CREATE TABLE IF NOT EXISTS banlist
                  (user_id INTEGER PRIMARY KEY, date TEXT)
                ''')
conn.commit()

# <-------------- SAVE USER -------------->
async def check_user(user_id: int):
    cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cursor.fetchone()

async def insert_user(name: str, username: str, user_id: int, date: str):
    cursor.execute(f"INSERT INTO users VALUES (?, ?, ?, ?)", (name, username, user_id, date))
    conn.commit()

async def save_user(name: str, username: str, user_id: int, date: str):
    user = await check_user(user_id)

    if not user:
        await insert_user(name, username, user_id, date)
    else:
        if (user[0] != name) or (user[1] != username):
            cursor.execute("UPDATE users SET name=?, username=? WHERE user_id=?", (name, username, user_id))
            conn.commit()
        else:
            pass

# <-------------- ADD / DELETE TO BANLIST -------------->
async def check_user_banlist(user_id: int):
    cursor.execute("SELECT * FROM banlist WHERE user_id=?", (user_id,))
    return cursor.fetchone()

async def insert_user_banlist(user_id, date):
    cursor.execute(f"INSERT INTO banlist VALUES (?, ?)", (user_id, date))
    conn.commit()

async def save_user_banlist(user_id: int, date: str):
    user = await check_user_banlist(user_id)

    if not user:
        await insert_user_banlist(user_id, date)
    else:
        pass

async def delete_banlist(user_id: int):
    user = await check_user(user_id)

    if user:
        cursor.execute("DELETE FROM banlist WHERE user_id = ?", (user_id,))
        conn.commit()
