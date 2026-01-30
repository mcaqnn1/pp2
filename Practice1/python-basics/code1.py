password = "1234"
tries = 3

while tries > 0:
    p = input("Пароль енгіз: ")
    if p == password:
        print("Кіру сәтті!")
        break
    else:
        tries -= 1
        print("Қате пароль. Қалған мүмкіндік:", tries)

if tries == 0:
    print("Блокталды!")
