import psycopg2
from psql.config import config



def insert_info(today,food,carbs,insulin,user_id):
    today = today.strftime('%Y-%m-%d')
    today = "'"+today+"'"
    food = "'"+food+"'"
    sql = f"""INSERT INTO info_table(user_id, date, food, carbs, insulin)
             VALUES({user_id}, {today}, {food}, {carbs}, {insulin} ) RETURNING info_log;"""
    conn = None
    info_log = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (today,food,carbs,insulin,user_id))
        # get the generated id back
        info_log = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return info_log

def insert_user(user_name, email_id):
    user_name = "'"+user_name+"'"
    email_id = "'"+email_id+"'"
    sql = f"""INSERT INTO user_table(user_name, email_id)
              VALUES ( {user_name}, {email_id}) 
              RETURNING user_id"""
    conn = None
    user_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (user_name,email_id))
        # get the generated id back
        user_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print("ERROR")
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return user_id

