def func(radius):
    pi = 3.14159
    area = pow(radius,2) * pi
    return f"{area:.2f}"
x = float(input())
print(func(x))