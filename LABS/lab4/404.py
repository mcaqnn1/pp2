def SquaresfromAtoB(a,b):
    for i in range(a, b + 1):
        print(pow(i,2))
a,b = map(int,input().split())
SquaresfromAtoB(a,b)