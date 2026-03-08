n = int(input())
arr = list(map(int, input().split()))

if any(x < 0 for x in arr):
    print("No")
else:
    print("Yes")