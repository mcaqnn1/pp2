from connect import create_connection

conn = create_connection()
cur = conn.cursor()

run = True
while run:
    EXIT = input("Введите exit для выхода из программы(иначе ENTER): ")
    if EXIT == "exit":
        run = False
        break

    FIRST_NAME = input("Your First Name: ")
    LAST_NAME = input("Your Last Name: ")
    GENDER = input("Your Gender: ")
    PHONE_NUMBER = input("Your Phone-Number: ")

    cur.execute(
        "INSERT INTO Users (first_name,last_name,gender,phone_number) VALUES (%s,%s,%s,%s)",
        (FIRST_NAME,LAST_NAME,GENDER,PHONE_NUMBER)
    )
    conn.commit()

    print("✅ Сохранено!\n")
conn.close()
cur.close()


    



      
    



