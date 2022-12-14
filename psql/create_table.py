import psycopg2
from psql.config import config

def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        DROP TABLE IF EXISTS info_table
        """,
        """
        DROP TABLE IF EXISTS user_table
        """,
        """
        DROP TABLE IF EXISTS carb_db
        """,
        """ 
        CREATE TABLE IF NOT EXISTS user_table (
                user_id SERIAL PRIMARY KEY,
                user_name VARCHAR(255),
                email_id VARCHAR(255)
                )
        """,
        """
        CREATE TABLE IF NOT EXISTS info_table (
                info_log SERIAL PRIMARY KEY,
                user_id INTEGER,
                date DATE NOT NULL,
                food VARCHAR(255) NOT NULL,
                quantity INTEGER,
                carbs REAL NOT NULL,
                insulin REAL NOT NULL,
                FOREIGN KEY (user_id)
                REFERENCES user_table (user_id)
                ON UPDATE CASCADE ON DELETE CASCADE
        )
        """,
        """ 
        CREATE TABLE IF NOT EXISTS carb_db (
                food_id SERIAL PRIMARY KEY,
                food VARCHAR(255) NOT NULL UNIQUE,
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


if __name__ == '__main__':
    create_tables()
