import sys

def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input().strip())

first = True
buf = []

for x in even_numbers(n):
    s = str(x)
    if first:
        buf.append(s)
        first = False
    else:
        buf.append("," + s)

    if len(buf) >= 1024:
        sys.stdout.write("".join(buf))
        buf.clear()

if buf:
    sys.stdout.write("".join(buf))