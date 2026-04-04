from connect import create_connection

conn = None
cur = None
try:
    conn = create_connection()
    cur = conn.cursor()
    cur.execute(
        '''
        create table users(
            id bigserial primary key,
            first_name varchar(50) not null,
            last_name varchar(50) not null,
            phone_number varchar(50) not null,
            email varchar(70),
            date_of_birth date not null);
        ''')
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()

