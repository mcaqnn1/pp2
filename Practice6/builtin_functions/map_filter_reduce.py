from functools import reduce

arr = [1,2,3,4,5]

print(list(map(lambda x: x + 1,arr)))
print(list(filter(lambda x: x > 2,arr)))
print(reduce(lambda x, y: x + y, arr)) #reduce берет все элементы списка a и складывает их в одно число.