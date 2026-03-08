txt = input()
ok = False
for x in range(len(txt)):
    if (('A' <= txt[0] and txt[0] <= 'Z') or ('a' <= txt[0] and txt[0] <= 'z')) and ('0' <= txt[len(txt) - 1] and txt[len(txt) - 1] <= '9'):
        ok = True
if ok:
    print("Yes")
else:
    print("No")