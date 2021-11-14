
import sqlite3
import datetime


con = sqlite3.connect("data.sqlite")
cur = con.cursor()
# cur.execute("CREATE TABLE dates( id INTEGER PRIMARY KEY, date DATE, clean BOOLEAN);")
cur.execute("INSERT INTO dates(date, clean) VALUES ('12.11.2021', 1);")
print(cur.execute("SELECT * FROM dates").fetchall())
# request = "SELECT * FROM users\
# WHERE chat_id={}".format(str(chat_id))
# usrs_with_id = cur.execute(request).fetchall()
# if len(usrs_with_id):
# return False
# request = "INSERT INTO users(username, chat_id)\
# '\n'VALUES({}, {})".format(username, str(chat_id))
# return True