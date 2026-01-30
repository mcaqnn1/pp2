n = int(input("Сан: "))
n = abs(n)
s = 0

while n > 0:
    s += n % 10
    n //= 10

print("Цифрлар қосындысы:", s)
