s = input()
res = []
for ch in s:
    if ch.isdigit():
        res.append(ch * 2)
    else:
        res.append(ch)
print(''.join(res))


    
        