# hello 76 world 11 ttt 26
s = list(map(str,input().split()))
arr = []
for x in s:
    if '0' < x and x < '9':
        arr.append(x)
print(max(arr))


