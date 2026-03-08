def lambda_expression(nums, array):
    for line in array:
        parts = line.split()
        op = parts[0]

        if op == "abs":
            nums = list(map(abs, nums))

        elif op == "add":
            val = int(parts[1])
            nums = list(map(lambda x: x + val, nums))

        elif op == "multiply":
            val = int(parts[1])
            nums = list(map(lambda x: x * val, nums))

        elif op == "power":
            val = int(parts[1])
            nums = list(map(lambda x: x ** val, nums))

    print(*nums)


n = int(input())  
nums = list(map(int, input().split()))

k = int(input())
array = [input().strip() for _ in range(k)]

lambda_expression(nums, array)



