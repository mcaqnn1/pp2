import re
email = input()
email_copy = email.split()
k = 0
ok_first = False
ok_second = False
pattern = re.escape("@")
if len(email_copy) == 1:
    for x in re.finditer(pattern,email):
        ok_first = True
        r = 0
if len(email_copy) > 1:
    for y in re.finditer(pattern,email):
        ok_second = True
        k += 1
if ok_first:
    print(email_copy[r])
elif ok_second:
    print(email_copy[k])
else:
    print("No email")







    


