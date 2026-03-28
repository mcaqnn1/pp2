import psycopg2

conn = None
cur = None
try:
    conn = psycopg2.connect(
        host = 'localhost',
        user = 'postgres',
        password = 'arsen0717',
        database = 'myapp'
    )
    cur = conn.cursor()
    cur.execute(
         """
         CREATE TABLE Users (
              id SERIAL PRIMARY KEY,
              first_name VARCHAR(50) NOT NULL,
              last_name VARCHAR(50) NOT NULL,
              gender VARCHAR(10),
              phone_number VARCHAR(50) UNIQUE NOT NULL);
         """)
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()
