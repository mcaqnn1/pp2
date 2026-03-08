txt = input()

count = 0
for i in range(len(txt)):
    if 'A' <= txt[i] and txt[i] <= 'Z':
        count += 1

print(count)