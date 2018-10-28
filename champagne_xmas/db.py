import psycopg2
from champagne_xmas import bcrypt
from random import randrange

DB = "champagne"
HOST = "localhost"
USER = "postgres"
PW = "3dc41885"
DNS = "dbname='{}' user='{}' host='{}' password='{}'".format(DB, USER, HOST, PW)

def all_users_here():
    sql_query = "SELECT COUNT(*) FROM users;"
    result = execute_sql(sql_query)
    return result[0][0] == 8 #number of ppl coming 

def get_existing_pair(username):
    sql_query = "SELECT pair FROM users WHERE username = %s;"
    data = (username, )
    result = execute_sql(sql_query, data)
    if result:
        return get_name(result[0][0])
    return None

def get_name(my_id):
    sql_query = "SELECT username FROM users WHERE userid = %s;"
    data = (my_id,)
    result = execute_sql(sql_query, data)
    if result:
        return result[0][0]
    return None

def get_pair(username):
    my_id = get_id(username)
    sql_query = "SELECT userid, username FROM users WHERE username != %s AND reserved = FALSE AND ( pair != %s OR pair IS NULL );"
    data = (username, my_id)
    result = execute_sql(sql_query, data)
    if result:
        ids = [i[0] for i in result]
        names = [i[1] for i in result]
        index = randrange(0, len(ids))
        sql_query = "UPDATE users SET pair = %s WHERE userid = %s"
        data = (ids[index], my_id)
        execute_sql(sql_query, data)
        sql_query = "UPDATE users SET reserved = TRUE WHERE userid = %s;"
        data = (ids[index],)
        execute_sql(sql_query, data)
        return names[index]
    return None

def get_id(username):
    sql_query = "SELECT userid FROM users WHERE username = %s;"
    data = (username,)
    result = execute_sql(sql_query, data)
    return result[0][0]

def load_user(username, password):
    sql_query = "SELECT password FROM users WHERE username = %s;"
    data = (username,)
    result = execute_sql(sql_query, data)
    if result:
        pw_hash = result[0][0].encode('utf-8')
        return bcrypt.check_password_hash(pw_hash, password)
    return False   

def build_insert(username, password):
    if check_existing_name(username):
        return False
    sql_query = "INSERT INTO users VALUES (DEFAULT, %s, %s);"
    data = (username, password)
    execute_sql(sql_query, data)
    return True

def check_existing_name(username):
    sql_query = "SELECT username FROM users WHERE username = %s"
    data = (username,)
    result = execute_sql(sql_query, data)
    return True if result else False

def get_users():
    sql_query = "SELECT username FROM users;"
    result = execute_sql(sql_query)
    if result:
        return [i[0] for i in result]
    return None

def execute_sql(query, data = None):
    conn = None
    try:
        conn = psycopg2.connect(DNS)
    except psycopg2.OperationalError as error:
        print("Execute query failed: " + error)
    else:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query) if data == None else cursor.execute(query, data)
            if cursor.description != None:
                return cursor.fetchall()
    finally:
        if conn:
            conn.close()