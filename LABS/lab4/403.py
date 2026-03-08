def DivisibilityCheck(num):
    for i in range(num + 1):
        if i % 3 == 0 and i % 4 == 0:
            print(i,end=" ")
num = int(input())
DivisibilityCheck(num)