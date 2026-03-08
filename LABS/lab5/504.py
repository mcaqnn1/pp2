txt = input()

for x in range(len(txt)):
    if '0' <= txt[x] and txt[x] <= '9':
        print(txt[x], end=" ")