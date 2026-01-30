a = float(input("a: "))
op = input("Амалы (+, -, *, /): ")
b = float(input("b: "))

if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
elif op == "*":
    print(a * b)
elif op == "/":
    if b == 0:
        print("0-ге бөлуге болмайды")
    else:
        print(a / b)
else:
    print("Белгі дұрыс емес")
