import datetime

import psycopg2 as psql
from get_db_config_from_url import get_db_config_from_url


def register(username, chat_id):
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    check_request = "SELECT * FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(check_request)
    users_with_this_id = cur.fetchall()
    if len(users_with_this_id):
        return False
    insert_request = "INSERT INTO users(username, chat_id, clean_days, all_days) VALUES('{}', '{}', '{}', '{}')". \
        format(username, str(chat_id), 0, 0)
    cur.execute(insert_request)
    con.commit()
    return True


def add_score(date, result, chat_id):
   
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT id FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(request)
    user_id = cur.fetchall()
    if not len(user_id):
        return False
    check_request = "SELECT clean_days, all_days FROM users WHERE chat_id = '{}'".format(chat_id)
    cur.execute(check_request)
    results = cur.fetchall()

    is_date_filled_req = "SELECT date FROM archive WHERE date = '{}' AND user_id = {}".format(
    	date, user_id[0][0])
    cur.execute(is_date_filled_req)
    is_date = cur.fetchall()

    if len(is_date):
        print('right')
        prev_value_req = "SELECT is_clean FROM archive WHERE date = '{}' AND user_id = {}".format(date, user_id[0][0])
        cur.execute(prev_value_req)
        prev_value = cur.fetchall()[0][0]

        cur.execute("UPDATE users SET clean_days = {} WHERE chat_id = '{}'".format(
            results[0][0] - prev_value + result, chat_id))

        cur.execute("UPDATE archive SET is_clean = '{}' WHERE user_id = '{}' AND date = '{}'".format(
        	result, user_id[0][0], date) )



        
    else:

    	cur.execute("INSERT INTO archive(user_id, date, is_clean)" \
    				"VALUES ({}, '{}', {})".format(
    				user_id[0][0], date, result))

    	cur.execute("UPDATE users SET clean_days = {}, all_days = {} WHERE chat_id = '{}'".format(
            results[0][0] + result, results[0][1] + 1, chat_id))
  	

    con.commit()
    return True


def get_score(chat_id):

    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT clean_days, all_days FROM users WHERE chat_id = '{}'".format(str(chat_id))
    cur.execute(request)
    all_days, clean_days = cur.fetchall()[0]

    return all_days, clean_days


def get_stats(chat_id, task_number=0):
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    if not task_number:
        request = "SELECT task_num, right_answers, all_answers FROM stats\
        \nWHERE user_id in (SELECT id FROM users\
        \nWHERE chat_id = '{}') ORDER BY task_num".format(str(chat_id))
    else:
        request = "SELECT task_num, right_answers, all_answers FROM stats\
                \nWHERE user_id in (SELECT id FROM users\
                \nWHERE chat_id = '{}') AND task_num = {} ORDER BY task_num".format(str(chat_id), task_number)
    cur.execute(request)
    result = cur.fetchall()
    if not len(result):
        return False
    count_of_answers_dict = {}
    for task_number, right_answers, all_answers in result:
        count_of_answers_dict[str(task_number)] = (right_answers, all_answers)
    return count_of_answers_dict


def get_all_users_chat_ids():
    con = psql.connect(**get_db_config_from_url())
    cur = con.cursor()
    request = "SELECT chat_id FROM users"
    cur.execute(request)
    chat_ids = cur.fetchall()
    return chat_ids


if __name__ == '__main__':
    print(get_activity('1830477841'))
