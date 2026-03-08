txt = input().split()
i = txt.index("Age:")
print(" ".join(txt[1:i]).strip(","), *txt[i+1:])

