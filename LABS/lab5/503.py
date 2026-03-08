import re

txt = input()
word = input()
res = 0

pattern = re.escape(word)

for m in re.finditer(pattern,txt):
    res += 1
print(res)
 
