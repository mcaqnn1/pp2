s = input().strip()
print("Valid" if all((ord(c)-48) % 2 == 0 for c in s) else "Not valid")
