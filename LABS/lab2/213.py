n = int(input().strip())

if n <= 1:
    print("No")
elif n <= 3:
    print("Yes")
elif n % 2 == 0 or n % 3 == 0:
    print("No")
else:
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            print("No")
            break
        i += 6
    else:
        print("Yes")
