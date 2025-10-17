import psycopg2
import psycopg2.extras

def connect_db():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="drone_app",
            user="postgres",
            password="abc123"
        )
        print('connected')
        return conn
    except Exception as e:
        print(e)
        return False