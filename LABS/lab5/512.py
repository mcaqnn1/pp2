import re

s = input()
res = re.findall(r'\d{2,}', s)
print(' '.join(res))