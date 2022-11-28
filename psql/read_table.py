import psycopg2
from psql.config import config
import pandas as pd



def get_info(user_id):
    df = pd.DataFrame([],columns=["date", "food", "carbs", "insulin"])
    sql = f"""
            SELECT date, food, carbs, insulin 
            FROM info_table 
            WHERE user_id = {user_id}
            ORDER BY date
           """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(user_id))
        print("The number of items: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            df.loc[len(df)] = list(row)
            row = cur.fetchone()

        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return df
    
def get_all_info():
    df = pd.DataFrame([],columns=["user_id", "date", "food", "carbs", "insulin"])
    sql = f"""
            SELECT user_id, date, food,carbs, insulin 
            FROM info_table
            ORDER BY date
           """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        while row is not None:
            df.loc[len(df)] = list(row)
            row = cur.fetchone()

        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return df
    
    
def get_all_users():
    df = pd.DataFrame([],columns=["user_id", "name", "email"])
    sql = f"""
            SELECT user_id, user_name, email_id 
            FROM user_table
            ORDER BY user_id
           """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql)
        row = cur.fetchone()

        while row is not None:
            df.loc[len(df)] = list(row)
            row = cur.fetchone()

        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return df
  
