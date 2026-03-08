num = int(input())
numbers = list(map(int,input().split()))
numberss = set(numbers)
arr = []
for x in numberss:
    arr.append(x)
res = sorted(arr)
print(*res,end=" ")