import re

s = input()
res = re.findall(r'\d{2}/\d{2}/\d{4}', s)
print(len(res))