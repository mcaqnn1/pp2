import sys

def fib_gen(n: int):
    a, b = 0, 1
    for _ in range(n):
        yield a
        a, b = b, a + b

n = int(input().strip())

first = True
for x in fib_gen(n):
    if first:
        sys.stdout.write(str(x))
        first = False
    else:
        sys.stdout.write("," + str(x))