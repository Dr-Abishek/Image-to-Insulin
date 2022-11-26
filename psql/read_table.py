# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 15:49:15 2022

@author: AbishekH
"""
import psycopg2
from config import config

def get_info(user_id):
    
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
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
if __name__ == '__main__':
    get_info(user_id=1)