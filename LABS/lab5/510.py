import re
txt = input().split()

ok = False
for x in txt:
    if re.search(r"dog",x) or re.search(r"cat",x):
        ok = True

if ok:
    print("Yes")
else:
    print("No")