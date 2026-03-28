import csv
from connect import create_connection

def insert_danns(csv_file = 'person.csv'):
    conn = create_connection()
    cur = conn.cursor()
    with open(csv_file,'r') as danns:
        reader = csv.DictReader(danns)
        for row in reader:
            cur.execute("insert into Person (id,first_name,last_name,email,gender,date_of_birth,country_of_birth) values (%s,%s,%s,%s,%s,%s,%s)",
                (row['id'],row['first_name'],row['last_name'],row['email'],row['gender'],row['date_of_birth'],row['country_of_birth'])
            )
            conn.commit()
        conn.commit()
        conn.close()
        cur.close()
if __name__ == '__main__':
    insert_danns()
