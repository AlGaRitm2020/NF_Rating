from pprint import pprint

import psycopg2
import datetime
from get_db_config_from_url import get_db_config_from_url

conn = psycopg2.connect(**get_db_config_from_url())
cur = conn.cursor()
# --- drop tables ---
""" 
cur.execute('DROP TABLE stats;')
cur.execute('DROP TABLE users;') 

"""

# cur.execute('DROP TABLE activity;')
# --- create tables ---

"""
cur.execute("create table users(id serial primary key, username VARCHAR, chat_id  VARCHAR unique, clean_days INTEGER, all_days INTEGER);")
cur.execute("create table stats(id serial primary key, user_id INTEGER references users, task_num INTEGER, right_answers INTEGER, all_answers INTEGER);")
"""
#cur.execute("create table archive(id serial primary key, user_id INTEGER references users, date DATE, is_clean INTEGER);")

# --- insert old users ---
"""
cur.execute("INSERT INTO users (username, chat_id) VALUES ('@AlGaRitm2020', '1830477841');")
cur.execute("INSERT INTO users (username, chat_id, clean_days, all_days) VALUES ('@albert_gareev', '1283628271', 1, 1);")
"""

# print(type(datetime.date.today()))
# cur.execute("INSERT INTO activity (user_id, date, right_answers) VALUES (8, '{}', 7);".format('2021-07-07'))
# --- delete data from tables ---
"""
cur.execute("DELETE FROM stats;")
cur.execute("DELETE FROM users WHERE id = 4;")
"""


# cur.execute("DELETE FROM archive;")
# cur.execute("DELETE FROM users;")
# cur.execute("UPDATE stats  SET (right_answers, all_answers) =  (12, 20) WHERE user_id = 8;")
# cur.execute("INSERT INTO stats (task_num, user_id) VALUES (3, 8);")

cur.execute("SELECT * FROM users;")
print('users', 'id, username, chat_id, clean_days, all_days', sep='\n')
pprint(cur.fetchall())

cur.execute("SELECT * FROM archive;")
print('users', 'id, user_id, date, is_clean', sep='\n')
pprint(cur.fetchall())
"""# --- select data from users ---
cur.execute("SELECT * FROM users;")
print('users', 'id, username, chat_id', sep='\n')
pprint(cur.fetchall())

# --- select data from stats ---
cur.execute("SELECT * FROM stats WHERE user_id = 8;")
print('stats', 'id, user_id, task, right_answers, all_answers', sep='\n')
pprint(cur.fetchall())

# --- select data from users ---
cur.execute("SELECT * FROM activity;")
print('id', 'user_id, date', sep='\n')
pprint(cur.fetchall()) """

conn.commit()
cur.close()
conn.close()
