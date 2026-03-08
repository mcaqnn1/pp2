import re
s = "()[]{}"

pattern_1 = re.escape("()")
pattern_2 = re.escape("{}")
pattern_3 = re.escape("[]")

found = False
for x in re.findall(pattern_1,s) or re.findall(pattern_2,s) or re.findall(pattern_3,s):
    found = True

if found:
    print("true")
else:
    print("false")