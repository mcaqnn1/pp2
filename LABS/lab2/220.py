n = int(input().strip())
doc = {}

for _ in range(n):
    parts = input().split()
    if parts[0] == "set":
        key = parts[1]
        value = parts[2]
        doc[key] = value
    else:  # get
        key = parts[1]
        if key in doc:
            print(doc[key])
        else:
            print(f"KE: no key {key} found in the document")
