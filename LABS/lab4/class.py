'''
class Person:
    def __init__(self,name,age,country):
        self.name = name
        self.age = age
        self.counrty = country
    
    def func(self):
        print(f"My name is {self.name} and {self.age} old. I'm from {self.counrty}")
name, age, coun = map(str,input().split())
m = Person(name,age,coun)
m.func()
'''
'''
class Myclass:
    def __iter__(self):
        self.num = 0
        return self
    
    def __next__(self):
        while self.num <= 50:
            x = self.num
            self.num += 1
            if x % 2 == 0:
                return x
        raise StopIteration
p = Myclass()
myiter = iter(p)
for x in myiter:
    print(x, end=" ")
'''
'''
def subarraySum(nums, k):
    answer = 0
    for start in range(len(nums)):
        for end in range(start,len(nums)):
            subarray_sum = 0
            for i in range(start, end + 1):
                subarray_sum += nums[i]
            if subarray_sum == k:
                answer += 1
    return answer
nums = [1,1]
k = 3
print(subarraySum(nums,k)
'''

try:
    print("hello world")
finally:
    print(1)
        



