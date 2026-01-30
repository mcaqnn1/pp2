nums = list(map(int, input("Сандарды енгіз: ").split()))
count = 0

for x in nums:
    if x % 2 == 0:
        count += 1

print("Жұп сандар саны:", count)
