from connect import create_connection
import csv

conn = None
cur = None
try:
    def insert_for_db(csv_file='contacts.csv'):
        conn = create_connection()
        cur = conn.cursor()
        with open (csv_file,'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute("insert into users (id,first_name,last_name,phone_number,email,date_of_birth) values (%s,%s,%s,%s,%s,%s)",
                           (row['id'],row['first_name'],row['last_name'],row['phone_number'],row['email'],row['date_of_birth']) 
                           )
            conn.commit()
    if __name__ == '__main__':
        insert_for_db()
except Exception as error:
    print(error)  
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()
    
