from connect import create_connection

conn = None
cur = None
try:
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("update users set phone_number = %s where id = %s",
                ("+77054212637","5"))
    conn.commit()
except Exception as error:
    print(error)
finally:
    if conn is not None:
        conn.close()
    if cur is not None:
        cur.close()