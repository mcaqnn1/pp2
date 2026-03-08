num = int(input())
s = list(map(str,input().split()))
print(max(s, key=len))
