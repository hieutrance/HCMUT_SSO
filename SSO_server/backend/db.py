import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        user=os.getenv("DB_USERNAME"),
        password=os.getenv("DB_PASS"),
        database=os.getenv("DB_NAME")
    )
    
def execute_sql(query, params=None, fetch_one=False, fetch_all=False):
    conn = None
    cursor = None
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params)

        # SELECT
        if fetch_one:
            return cursor.fetchone()

        if fetch_all:
            return cursor.fetchall()

        # INSERT/UPDATE/DELETE
        conn.commit()
        return cursor.rowcount

    except Error as e:
        print("MySQL error:", e)
        return None

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
