def func(num_one,num_two):
    result = num_one - num_two
    if result >= 0:
        return result
    else:
        return "Insufficient Funds"
a,b = map(int,input().split())
print(func(a,b))
