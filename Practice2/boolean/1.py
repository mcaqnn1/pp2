ok = False
def a(x):
    while x > 0:
        if x % 2 == 0:
            ok = True
            break
        x /=10
q = int(input())
a(q)
if ok:
    print("Valid")
else:
    print("Not valid")
