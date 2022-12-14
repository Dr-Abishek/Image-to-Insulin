import psycopg2
from psql.config import config
            
def search_carb_info_db(food_item):
    food_item = "'"+food_item+"'"
    sql = f"""
            SELECT food_id, food, carbs 
            FROM carb_db 
            WHERE food = {food_item}
           """
    conn = None
    food_id = None
    carbs = None        
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,food_item)
        row = cur.fetchone()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return row[0], row[2]
      
def update_carb_info_db(food_item,carbs_g):
   
    food_item = "'"+food_item+"'"
    sql = f"""INSERT INTO carb_db(food, carbs)
             VALUES({food_item}, {carbs_g})
             RETURNING food_id"""
    conn = None
    food_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql, (food_item,carbs_g))
        # get the generated id back
        food_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return food_id
       
