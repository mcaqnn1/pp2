import re
s = input().split()
word = input()

pattern = re.escape(word)

ok = False
for x in s:
    if re.search(pattern,x):
        ok = True

if ok:
    print("Yes")
else:
    print("No")