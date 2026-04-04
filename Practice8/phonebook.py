from connect import create_connection

def run_sql_file(filename):
    conn = create_connection()
    cur = conn.cursor()
    with open(filename, "r") as file:
        sql = file.read()
    cur.execute(sql)
    try:
        result = cur.fetchall()
        for row in result:
            print(row)
    except:
        print("Запрос выполнен")
    conn.commit()
    cur.close()
    conn.close()

def new_users_sql_file(filename):
    conn = create_connection()
    cur = conn.cursor()

    with open(filename,"r") as NewUsers:
        sql = NewUsers.read()

    cur.execute(sql)
    conn.commit()
    conn.close()
    cur.close()

def delete_users_sql_file(filename):
    conn = create_connection()
    cur = conn.cursor()

    with open(filename,"r") as DeleteUsers:
        sql = DeleteUsers.read()

    cur.execute(sql)
    conn.commit()
    conn.close()
    cur.close()


if __name__ == "__main__":
    run_sql_file("request.sql")
    new_users_sql_file("new_users.sql")
    delete_users_sql_file("delete_users.sql")