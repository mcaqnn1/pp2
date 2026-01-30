import random

choices = ["тас", "қайшы", "қағаз"]
bot = random.choice(choices)

user = input("тас/қайшы/қағаз: ").lower()

if user not in choices:
    print("Дұрыс енгіз: тас, қайшы немесе қағаз")
else:
    print("Бот таңдады:", bot)
    if user == bot:
        print(" Тең!")
    elif (user == "тас" and bot == "қайшы") or (user == "қайшы" and bot == "қағаз") or (user == "қағаз" and bot == "тас"):
        print("Сен жеңдің!")
    else:
        print("Бот жеңді!")
