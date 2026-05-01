from connect import create_connection
import csv
import json

def create_table_users():
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        DATABASE_TABLE_USERS = '''
            CREATE TABLE IF NOT EXISTS users(
                id bigserial primary key,
                first_name varchar(50) not null,
                last_name varchar(50),
                phone_number varchar(30) not null,
                email varchar(70) not null,
                date_of_birth date
                );
            '''
        cur.execute(DATABASE_TABLE_USERS)
        conn.commit()
        
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()
            
def add_users(filename = 'contacts.csv'):
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute("""INSERT INTO users(id,first_name,last_name,phone_number,email,date_of_birth) VALUES (%s,%s,%s,%s,%s,%s)""",
                            (row['id'],row['first_name'],row['last_name'],row['phone_number'],row['email'],row['date_of_birth'])
                            )
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

def create_table_groups():
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        DATABASE_TABLE_GROUPS = '''
            CREATE TABLE IF NOT EXISTS groups(
                id SERIAL PRIMARY KEY,
                name VARCHAR(50) UNIQUE NOT NULL
                );
            '''
        cur.execute(DATABASE_TABLE_GROUPS)
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

def add_column_for_users():
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute('''
            ALTER TABLE users
                ADD COLUMN group_id INTEGER REFERENCES groups(id);
            ''')
        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

def create_table_phones():
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        DATABASE_TABLE_PHONES = '''
        CREATE TABLE IF NOT EXISTS phones(
            id         SERIAL PRIMARY KEY,
            contact_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            phone      VARCHAR(20)  NOT NULL,
            type       VARCHAR(10)  CHECK (type IN ('home', 'work', 'mobile'))
            );
        '''
        cur.execute(DATABASE_TABLE_PHONES)
        conn.commit()

    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

def export_users_to_json(filename="users.json"):
    conn = None
    cur = None
    try:
        conn = create_connection()
        cur = conn.cursor()
        cur.execute("SELECT id,first_name,last_name,phone_number,email,date_of_birth FROM users")
        rows = cur.fetchall()

        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "first_name": row[1],
                "last_name":row[2],
                "phone_number": row[3],
                "email": row[4],
                "date_of_birth": str(row[5] if row[5] else None)
            })
        with open(filename,"w") as f:
            json.dump(users,f,indent = 4, ensure_ascii=False)
    
    except Exception as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
        if cur is not None:
            cur.close()

if __name__ == '__main__':
    create_table_users()
    #add_users()
    create_table_phones()
    create_table_groups()
    #add_column_for_users()
    export_users_to_json()

