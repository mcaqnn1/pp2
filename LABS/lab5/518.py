txt = input()

find = input()

res = 0
for i in range(len(txt)):
    if txt[i] == find:
        res += 1
print(res)