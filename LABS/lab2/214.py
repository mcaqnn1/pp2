n = int(input().strip())
a = list(map(int, input().split()))

freq = {}
for x in a:
    freq[x] = freq.get(x, 0) + 1

best_val = None
best_cnt = -1

for x, c in freq.items():
    if c > best_cnt or (c == best_cnt and (best_val is None or x < best_val)):
        best_cnt = c
        best_val = x

print(best_val)

