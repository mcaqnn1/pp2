import psycopg2

conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = 'localhost',
        database = 'practice',
        user = 'postgres',
        password = 'arsen0717'
    )
    cur = conn.cursor()
    cur.execute('''
            create table Person (
	            id INT PRIMARY KEY,
	            first_name VARCHAR(50) NOT NULL,
	            last_name VARCHAR(50) NOT NULL,
	            email VARCHAR(100),
	            gender VARCHAR(50) NOT NULL,
	            date_of_birth DATE NOT NULL,
	            country_of_birth VARCHAR(50) NOT NULL);
                ''')
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()


    