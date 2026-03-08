num = int(input())
arr = []
for i in range(num):
    x = str(input())
    arr.append(x)
students = set(arr)
print(len(students))