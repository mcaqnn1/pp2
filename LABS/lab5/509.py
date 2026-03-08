txt = input().split()

count = 0
for x in range(len(txt)):
    if len(txt[x]) == 3:
        count+=1
print(count)
