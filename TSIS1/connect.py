from config import get_db_config
import psycopg2
def create_connection():
    db_config = get_db_config()
    conn = psycopg2.connect(**db_config)
    return conn
