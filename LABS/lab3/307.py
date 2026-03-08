import math
def coordinates(x1,y1,x2,y2,x3,y3):
    x,y = x1,y1
    x1,y1 = x2,y2
    a = x3 - x2
    b = y3 - y2
    c = math.sqrt(pow(a,2) + pow(b,2))
    print(f"({x}, {y})\n({x2}, {y2})\n{c:.2f}")
x1,y1 = map(int, input().split())
x2,y2 = map(int, input().split())
x3,y3 = map(int, input().split())
coordinates(x1,y1,x2,y2,x3,y3)