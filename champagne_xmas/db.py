import psycopg2
import urllib
import os
from champagne_xmas import bcrypt
from random import randrange


def get_roomname(roomid):
    sql_query = "SELECT roomname FROM rooms WHERE roomid = %s;"
    data = (roomid,)
    result = execute_sql(sql_query, data)
    if result:
        return result[0][0]
    return None

def save_room(roomname, vipcode, letszam):
    sql_query = "SELECT roomname FROM rooms WHERE roomname = %s;"
    data = (roomname,)
    result = execute_sql(sql_query, data)
    if result:
        return False
    sql_query = "INSERT INTO rooms VALUES(default, %s, %s, %s);"
    data = (roomname, vipcode, int(letszam))
    execute_sql(sql_query, data)
    return True

def all_users_here(roomid):
    print(roomid)
    sql_query = "SELECT COUNT(*) FROM users WHERE roomid = %s;"
    data = (int(roomid),)
    result = execute_sql(sql_query, data)

    sql_query = "SELECT letszam FROM rooms WHERE roomid = %s;"
    data = (int(roomid),)
    result1 = execute_sql(sql_query, data)

    return result[0][0] == result1[0][0]

def get_existing_pair(username, roomid):
    sql_query = "SELECT pair FROM users WHERE username = %s AND roomid = %s;"
    data = (username, roomid)
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

def get_pair(username, roomid):
    my_id = get_id(username, roomid)
    sql_query = "SELECT userid, username FROM users WHERE username != %s AND reserved = FALSE AND ( pair != %s OR pair IS NULL ) AND roomid = %s;"
    data = (username, my_id, roomid)
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

def get_id(username, roomid):
    sql_query = "SELECT userid FROM users WHERE username = %s AND roomid = %s;"
    data = (username, roomid)
    result = execute_sql(sql_query, data)
    return result[0][0]

def load_user(username, password):
    sql_query = "SELECT password, roomid FROM users WHERE username = %s;"
    data = (username,)
    result = execute_sql(sql_query, data)
    if result:
        for res in result:
            pw_hash = res[0].encode('utf-8')
            if bcrypt.check_password_hash(pw_hash, password):
                return res[1]
    return False   

def build_insert(username, password, vipcode):
    result = check_room(vipcode)
    if result:
        if check_existing_name(username, result):
            return "nev"
        sql_query = "INSERT INTO users VALUES (DEFAULT, %s, %s, null, false, %s);"
        data = (username, password, result)
        execute_sql(sql_query, data)
        return "siker"
    return "room"

def check_room(vipcode):
    sql_query = "SELECT vipcode, roomid FROM rooms WHERE vipcode = %s;"
    data = (vipcode,)
    result = execute_sql(sql_query, data)
    if result:
        return result[0][1]
    return False

def check_existing_name(username, roomid):
    sql_query = "SELECT username FROM users WHERE username = %s AND roomid = %s;"
    data = (username, roomid )
    result = execute_sql(sql_query, data)
    return True if result else False

def get_users( roomid ):
    sql_query = "SELECT username FROM users WHERE roomid = %s;"
    data = (roomid, )
    result = execute_sql(sql_query, data)
    if result:
        return [i[0] for i in result]
    return None

def execute_sql(query, data = None):
    conn = None
    try:
        urllib.parse.uses_netloc.append('postgres')
        url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
    except psycopg2.OperationalError as error:
        print("Execute query failed ajjaj: " + error)
    else:
        conn.autocommit = True
        with conn.cursor() as cursor:
            cursor.execute(query) if data == None else cursor.execute(query, data)
            if cursor.description != None:
                return cursor.fetchall()
    finally:
        if conn:
            conn.close()
