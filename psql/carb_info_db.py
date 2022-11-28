import psycopg2
from psql.config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """ 
        CREATE TABLE IF NOT EXISTS carb_db (
                food_id SERIAL PRIMARY KEY,
                food VARCHAR(255) NOT NULL,
                carbs REAL NOT NULL
                )
        """
        )
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            
def carb_info_db(food):
    sql = f"""
            SELECT carbs 
            FROM carb_db 
            WHERE food = {food}
           """
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute(sql,(food))
        
        carbs = cur.fetchone()
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        return carbs
      
def update_carb_info_db(food_item,carbs_g):
    #create_tables()
    food_item = "'"+food_item+"'"
    sql = f"""INSERT INTO info_table(food, carbs)
             VALUES({food_item}, {carbs_g})
             RETURNING food_id"""
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
        food_id = cur.execute(sql, (food_item,carbs_))
        # get the generated id back
        cur.fetchone()[0]
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
       
